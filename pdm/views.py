import datetime
import os
from pdm.forms import LoginForm, RegistrationForm, ChangeableForm
import werkzeug
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.http import FileResponse, StreamingHttpResponse
from django.conf import settings
from encrypted_files.base import EncryptedFile
from django.views.decorators.csrf import csrf_protect

from pdm.models import AccessRequest, Document, User, VerificationRequest
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.utils.translation import gettext_lazy as _

from pdm.tools import extractPageNumber


@login_required
def index(request):
    docs = list(Document.objects.filter(owner=request.user))
    docs.sort(key=lambda x: x.uploaded_at, reverse=True)
    return render(request, 'pdm/index.html', {"documents": docs})


def getAccessibleDocuments(user: User) -> list:
    """Return a list of documents that the user has access to."""
    if user.role == User.DOCTOR:
        docs = Document.objects.filter(owner=user)
        approved_access = AccessRequest.objects.filter(
            doctor=user, approved=True)
        for req in approved_access:
            docs = docs | Document.objects.filter(Q(owner=req.patient) & Q(
                uploaded_at__gte=req.period_start) & Q(uploaded_at__lte=req.period_end) & Q(sensitive=False))
        return docs
    elif user.role == User.PATIENT:
        return Document.objects.filter(owner=user)
    else:
        return []


@login_required
def docs(request):
    docs = getAccessibleDocuments(request.user)
    status = request.session.pop("status", None)
    return render(request, 'pdm/docs.html', {"documents": docs, "status": status or ""})


@login_required
@csrf_protect
def upload(request):
    error_message = None
    if request.method == 'POST':
        if 'file' in request.FILES:
            sensitive = bool(request.POST.get('is_sensitive', False))
            print(sensitive)
            file = request.FILES['file']
            file_format: str = file.name.split('.')[-1]
            allowed: list = settings.ACCEPTED_DOCUMENT_EXTENSIONS
            if file_format.lower() in allowed and file.size <= 10000000:  # 10 MB
                doc = Document(owner=request.user, file=file,
                               name=file.name[:-len(file_format)-1], sensitive=sensitive)
                doc.save()
                request.session['status'] = "Successfully uploaded document"
                try:
                    tmp_path = "documents/tmp/"
                    tmp = f"{tmp_path}exif.{file_format}"
                    tmp = werkzeug.utils.secure_filename(tmp)
                    os.mkdir("documents/tmp")
                    with open(tmp, "wb") as f:
                        efile = EncryptedFile(doc.file).read()
                        f.write(efile)
                    pages = extractPageNumber(tmp)
                    os.unlink(tmp)
                    os.rmdir(tmp_path)
                    doc.pages = pages
                    doc.save()
                except Exception as e:
                    print(e)
                    pass
                return redirect('docs')
            else:
                error_message = "File is not allowed or too big"
        else:
            error_message = 'No file selected'
    return render(request, 'pdm/new-doc.html', {"upload_error": error_message or "", "allowed": ", ".join(["." + e for e in settings.ACCEPTED_DOCUMENT_EXTENSIONS])})


@login_required
def preview(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
    if doc.owner != request.user and doc not in getAccessibleDocuments(request.user):
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "message": "You do not have permission to view this document"}})

    if doc.file.name.split('.')[-1].lower() in settings.NO_PREVIEW_DOCUMENT_EXTENSIONS:
        return redirect('download', doc_id=doc_id)

    def get_type(filename):
        ext = filename.split('.')[-1]
        if ext == 'pdf':
            return 'application/pdf'
        elif ext == 'jpg' or ext == 'jpeg':
            return 'image/jpeg'
        elif ext == 'png':
            return 'image/png'
        else:
            return 'application/octet-stream'
    return StreamingHttpResponse(EncryptedFile(doc.file), content_type=get_type(doc.file.path), headers={'Content-Disposition': 'inline; filename=' + doc.name + '.' + doc.file.name.split('.')[-1]})


@login_required
def download(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
    if request.user != doc.owner and doc not in getAccessibleDocuments(request.user):
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the owner of this document"}})
    return FileResponse(EncryptedFile(doc.file), as_attachment=True, filename=doc_id + "." + doc.file.path.split('.')[-1])


@login_required
def deleteDoc(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
    if not doc:
        return render(request, 'pdm/error.html', {"error": {"type": "Not Found", "code": 404, "message": "Document not found"}})
    if request.user != doc.owner:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the owner of this document"}})
    doc.file.delete()
    doc.delete()
    request.session['status'] = "Successfully deleted document"
    return redirect('docs')


@login_required
def profilePage(request):
    return render(request, 'pdm/profile.html')


@csrf_protect
def loginPage(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                if not user.verified:
                    sendVerificationEmail(
                        user, f"{'http' if settings.DEBUG else 'https'}://{request.get_host()}/")
                next_page = request.GET.get('next')
                return redirect(next_page or 'index')
        form.add_error(None, "Invalid username or password")
    return render(request, 'registration/login.html', {"form": form})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')


def sendVerificationEmail(user: User, base_url: str, callback: str = "accounts/verify"):
    if user.verified:
        return 1
    # token = default_token_generator.make_token(user)
    # assert default_token_generator.check_token(user, token)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = base_url + callback + f"/{uid}/{token}"
    mail = EmailMessage(
        'Verify your account',
        f'Please verify your account by clicking the following link: {link}',
        to=[user.email]
    )
    return mail.send()


@login_required
@csrf_protect
def editProfile(request):
    form = ChangeableForm(instance=request.user)

    if request.method == 'POST':
        form = ChangeableForm(request.POST, instance=request.user)
        print(form.changed_data, form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            if 'email' in form.changed_data:
                if User.objects.filter(email=user.email).exists():
                    form.add_error('email', 'Email already exists')
                else:
                    user.verified = False
                    sendVerificationEmail(
                        user, f"{'http' if settings.DEBUG else 'https'}://{request.get_host()}/")
                    user.save()
                    return redirect('profile')
            else:
                user.save()
                return redirect('profile')

    return render(request, 'pdm/edit-profile.html', {"form": form})


@csrf_protect
def registerPage(request):
    form = RegistrationForm()
    if request.user.is_authenticated: 
        return redirect('index')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                form.add_error('password2', 'Passwords do not match')
            elif User.objects.filter(email=user.email).exists():
                form.add_error('email', 'Email already in use')
            else:
                user.save()
                sendVerificationEmail(
                    user, f"{request.scheme}://{request.get_host()}/")
                return render(request, 'pdm/basic-out.html', {"title": "Confirm Mail", "heading": "Successfull Registration", "messages": ["Please confirm your email address to complete the registration"]})
    return render(request, 'registration/register.html', {"form": form})


@login_required
def logoutPage(request):
    logout(request)
    return redirect('index')


def verifyUser(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and not user.verified:
        if default_token_generator.check_token(user, token):
            user.verified = True
            user.save()
            return render(request, 'pdm/basic-out.html', {"title": "Email Confirmed", "heading": "Email Confirmed", "messages": ["Your email address has been confirmed"]})
        else:
            return render(request, 'pdm/basic-out.html', {"title": "Invalid Token", "heading": "Invalid Token", "messages": ["The confirmation link was invalid, possibly because it has already been used. Please request a new confirmation email."]})
    else:
        return render(request, 'pdm/basic-out.html', {"title": "Email Confirmation Failed", "heading": "Email Confirmation Failed", "messages": ["The confirmation link was invalid"]})


@login_required
@user_passes_test(lambda u: u.role == User.DOCTOR or u.role == User.PATIENT)
def requestAccess(request):
    context = dict()
    today = datetime.date.today()
    min_date = datetime.date.today(
    ) - datetime.timedelta(days=settings.MAX_PAST_DAYS_FOR_ACCESS_REQUEST)
    max_date = datetime.date.today(
    ) + datetime.timedelta(days=settings.MAX_FUTURE_DAYS_FOR_ACCESS_REQUEST)
    if request.method == 'POST':
        patient_mail = request.POST['patient-mail']
        period_start = request.POST['start-date']
        period_end = request.POST['end-date']
        patient = User.objects.filter(email=patient_mail).first()
        if not patient:
            return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "Patient not found"}})
        if patient.email == request.user.email:
            return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "You cannot request access to your own documents"}})
        period_start = datetime.datetime.strptime(
            period_start, '%Y-%m-%d').date()
        period_end = datetime.datetime.strptime(period_end, '%Y-%m-%d').date()
        if period_start > today or period_start < min_date or period_end > max_date or period_end < today:
            return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "Invalid date range"}})
        access_request = AccessRequest.objects.create(
            patient=patient, doctor=request.user, period_start=period_start, period_end=period_end)
        access_request.save()
        existing_candidates = AccessRequest.objects.filter(
            patient=patient, doctor=request.user).exclude(pk=access_request.pk)
        for candidate in existing_candidates:
            if candidate.period_start <= period_start and candidate.period_end >= period_end:
                access_request.delete()
                return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "You already have requested access to this patient's documents for this period"}})
        context['success'] = "Request sent"
    context['today'] = str(today)
    context['min_date'] = str(min_date)
    context['max_date'] = str(max_date)
    context['requests_sent'] = AccessRequest.objects.filter(
        doctor=request.user, approved=False).reverse()
    context['requests_for_approval'] = AccessRequest.objects.filter(
        patient=request.user, approved=False).reverse()
    if request.user.role == User.DOCTOR:
        context['requests_processed'] = AccessRequest.objects.filter(Q(doctor=request.user) | Q(
            patient=request.user), Q(approved=True) | Q(denied=True)).reverse()
    else:
        context['requests_processed'] = AccessRequest.objects.filter(
            Q(patient=request.user), Q(approved=True) | Q(denied=True)).reverse()
    return render(request, 'pdm/request-access.html', context)


@login_required
@user_passes_test(lambda u: u.role == User.DOCTOR or u.role == User.PATIENT)
def approveOrDeny(request, req_id, action="deny"):
    actions = ("approve", "deny")
    access_request = AccessRequest.objects.filter(pk=req_id).first()
    if not access_request:
        return render(request, 'pdm/error.html', {"error": {"type": "Not Found", "code": 404, "message": "Request not found"}})
    if request.user.role == User.DOCTOR and access_request.doctor != request.user:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the doctor in this request"}})
    if request.user.role == User.PATIENT and access_request.patient != request.user:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the patient in this request"}})
    if action not in actions:
        return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "Invalid action"}})
    if access_request.approved or access_request.denied:
        return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "Request already processed"}})
    if action == "approve":
        access_request.approved = True
        access_request.approved_or_denied_at = datetime.datetime.now()
    elif action == "deny":
        access_request.denied = True
        access_request.approved_or_denied_at = datetime.datetime.now()
    access_request.save()
    return redirect('request-access')


@login_required
@user_passes_test(lambda u: u.role == User.DOCTOR)
def deleteRequest(request, req_id):
    access_request = AccessRequest.objects.filter(pk=req_id).first()
    if not access_request:
        return render(request, 'pdm/error.html', {"error": {"type": "Not Found", "code": 404, "message": "Request not found"}})
    if request.user.role == User.DOCTOR and access_request.doctor != request.user:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the doctor in this request"}})
    access_request.delete()
    return redirect('request-access')


def get_check_url(state_code):
    states = settings.STATES_BY_CODE
    mapping = settings.STATE_DOCTOR_INDEX_MAPPING
    if state_code not in states.keys():
        return None
    return mapping[state_code]


@login_required
def requestVerify(request):
    context = dict()
    if request.method == 'POST':
        cooldown = settings.VERIFY_REQUEST_COOLDOWN  # in seconds
        last_request = VerificationRequest.objects.filter(
            target_user=request.user).order_by('-requested_at').first()
        if last_request and (datetime.datetime.now(datetime.timezone.utc) - last_request.requested_at).total_seconds() < cooldown:
            context['error'] = f"You have to wait {cooldown//(60*60)} hours before requesting another verification"
        else:
            m_role = request.POST['role']
            title = request.POST['title'] if 'title' in request.POST else None
            state = request.POST['state'] if 'state' in request.POST else None
            check_url = get_check_url(state)
            if not state or not check_url:
                context['error'] = "Invalid state"
            else:
                v_request = VerificationRequest.objects.create(
                    target_user=request.user, medical_role=m_role, title=title, check_url=check_url)
                v_request.save()
                context['success'] = "Request sent"
    context['states'] = settings.STATES_BY_CODE
    context['requests_sent'] = VerificationRequest.objects.filter(
        target_user=request.user).reverse()
    if request.user.role == User.VERIFICATOR:
        context['requests_for_approval'] = VerificationRequest.objects.filter(
            Q(approved=False) & Q(denied=False)).reverse()
        context['requests_processed'] = VerificationRequest.objects.filter(
            Q(approved=True) | Q(denied=True) & Q(processed_by=request.user)).reverse()
    return render(request, 'pdm/request-verify.html', context)


@login_required
@user_passes_test(lambda u: u.role == User.VERIFICATOR)
def approveOrDenyVerify(request, req_id, action="deny"):  # TODO: add reason for denial
    actions = ("approve", "deny", "revoke")
    v_request = VerificationRequest.objects.filter(pk=req_id).first()
    if not v_request:
        return render(request, 'pdm/error.html', {"error": {"type": "Not Found", "code": 404, "message": "Request not found"}})
    if action not in actions:
        return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "Invalid action"}})
    if (v_request.approved or v_request.denied) and action != "revoke":
        return render(request, 'pdm/error.html', {"error": {"type": "Bad Request", "code": 400, "message": "Request already processed"}})
    if action == "approve":
        v_request.approved = True
        v_request.processed_by = request.user
        v_request.processed_at = datetime.datetime.now()
        v_request.target_user.role = User.DOCTOR
        v_request.target_user.save()
    elif action == "deny":
        v_request.denied = True
        v_request.processed_by = request.user
        v_request.processed_at = datetime.datetime.now()
    elif action == "revoke":
        v_request.approved = False
        v_request.denied = True
        v_request.processed_by = request.user
        v_request.processed_at = datetime.datetime.now()
        v_request.target_user.role = User.PATIENT
        v_request.target_user.save()
    v_request.save()
    return redirect('request-verify')
