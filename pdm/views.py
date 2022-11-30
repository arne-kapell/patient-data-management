from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import FileResponse, StreamingHttpResponse
from django.conf import settings
from encrypted_files.base import EncryptedFile
from django.views.decorators.csrf import csrf_protect

from .models import Document
from django.contrib.auth import authenticate, login, logout


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
            file = request.FILES['file']
            file_format: str = file.name.split('.')[-1]
            allowed: list = settings.ACCEPTED_DOCUMENT_EXTENSIONS
            if file_format.lower() in allowed and file.size <= 10000000:  # 10 MB
                doc = Document(owner=request.user, file=file,
                               name=file.name[:-len(file_format)-1])
                doc.save()
                request.session['status'] = "Successfully uploaded document"
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

    def get_type(filename):
        ext = filename.split('.')[-1]
        if ext == 'pdf':
            return 'application/pdf'
        elif ext == 'docx':
            return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif ext == 'doc':
            return 'application/msword'
        elif ext == 'odt':
            return 'application/vnd.oasis.opendocument.text'
        elif ext == 'jpg' or ext == 'jpeg':
            return 'image/jpeg'
        elif ext == 'png':
            return 'image/png'
        else:
            return 'application/octet-stream'
    return StreamingHttpResponse(EncryptedFile(doc.file), content_type=get_type(doc.file.path), headers={'Content-Disposition': 'inline; filename=' + doc.name})


@login_required
def download(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
    if request.user != doc.owner:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the owner of this document"}})
    return FileResponse(EncryptedFile(doc.file), as_attachment=True, filename=doc_id + "." + doc.file.path.split('.')[-1])


@login_required
def deleteDoc(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
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
            print("Login failed")
            context['error'] = 'Wrong username or password'
    return render(request, 'pdm/login.html', context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect('index')
