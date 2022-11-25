import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

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
    return render(request, 'pdm/docs.html', {"documents": docs})


@login_required
def download(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
    if request.user != doc.owner:
        return render(request, 'pdm/error.html', {"error": {"type": "Permission Denied", "code": 403, "message": "You are not the owner of this document"}})
    response = HttpResponse(doc.file)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        doc.file.name.split('/')[-1])
    return response


@csrf_protect
def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
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
