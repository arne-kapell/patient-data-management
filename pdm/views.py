import datetime
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.http import FileResponse, StreamingHttpResponse
from django.conf import settings
from encrypted_files.base import EncryptedFile
from django.views.decorators.csrf import csrf_protect

from pdm.models import AccessRequest, Document, User
from django.contrib.auth import authenticate, login, logout

from django.utils.translation import gettext_lazy as _

from pdm.tools import extractPageNumber


@login_required
def index(request):
    docs = list(Document.objects.filter(owner=request.user))
    docs.sort(key=lambda x: x.uploaded_at, reverse=True)
    return render(request, 'pdm/index.html', {"documents": docs})


@login_required
def docs(request):
    docs = list(Document.objects.filter(owner=request.user))
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
    if doc.owner != request.user:
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
    if request.user != doc.owner:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the owner of this document"}})
    return FileResponse(EncryptedFile(doc.file), as_attachment=True, filename=doc_id + "." + doc.file.path.split('.')[-1])


@login_required
def deleteDoc(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
    if not doc.exists():
        return render(request, 'pdm/error.html', {"error": {"type": "Not Found", "code": 404, "message": "Document not found"}})
    if request.user != doc.owner:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the owner of this document"}})
    doc.file.delete()
    doc.delete()
    request.session['status'] = "Successfully deleted document"
    return redirect('docs')


@csrf_protect
def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context['success'] = "Login successful"
        else:
            context['error'] = 'Wrong username or password'
    return render(request, 'pdm/login.html', context)


@csrf_protect
def registerPage(request):
    _
    context = {
        "form": [
            {"id": "mail", "type": "email", "label": _("email address"), "placeholder": _(
                "Enter email"), "required": True, "value": "", "autofocus": True},
            {"id": "password", "type": "password", "label": _("password"), "placeholder": _(
                "Enter password"), "required": True, "value": ""},
            {"id": "password2", "type": "password", "label": _("repeat password"), "placeholder": _(
                "Repeat password"), "required": True, "value": ""},
            {"id": "first_name", "type": "text", "label": _("first name"), "placeholder": _(
                "Enter first name"), "required": False, "value": ""},
            {"id": "last_name", "type": "text", "label": _("last name"), "placeholder": _(
                "Enter last name"), "required": False, "value": ""},
        ]
    }
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST['mail']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if password != password2:
            context['error'] = "Passwords do not match"
        elif User.objects.filter(email=email).exists():
            context['error'] = "Email already in use"
        else:
            user = User.objects.create_user(
                email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('login')
    return render(request, 'registration/register.html', context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect('index')


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
        context['success'] = "Request sent"
    context['today'] = str(today)
    context['min_date'] = str(min_date)
    context['max_date'] = str(max_date)
    context['requests_sent'] = AccessRequest.objects.filter(
        doctor=request.user, approved=False).reverse()
    context['requests_for_approval'] = AccessRequest.objects.filter(
        patient=request.user, approved=False).reverse()
    return render(request, 'pdm/request-access.html', context)
