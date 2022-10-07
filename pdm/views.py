from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

from .models import Document
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'pdm/index.html', {"a": 1, "b": 2})


@login_required
def docs(request):
    docs = Document.objects.all()
    url = docs[0].file.url
    print(url)
    return render(request, 'pdm/docs.html', {"documents": docs})


@login_required
def docView(request, doc_id):
    doc = Document.objects.get(pk=doc_id)
    context = {
        "uid": doc.uid,
        "owner": doc.owner,
        "url": doc.file.url
    }
    return render(request, 'pdm/document.html', context)


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
            # return redirect('index')
        else:
            print("Login failed")
            context['error'] = 'Wrong username or password'
    return render(request, 'pdm/login.html', context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect('index')
