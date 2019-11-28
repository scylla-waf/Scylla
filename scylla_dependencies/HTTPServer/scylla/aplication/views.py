from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.views import generic
from .forms import UserCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Request

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    return redirect('/')

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()

            if user is not None:
                do_login(request, user)
                return redirect('/')
    
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    return render(request, "register.html", {'form': form})

def login(request):
    logout(request)
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                return redirect('index.html')

    return render(request, "login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def requests(request):
    Request.objects.all().delete()
    manf = open("scylla_dependencies/WAF/log/petition.log")
    objetos = []
    for f in manf:
        if f.rstrip('\n')=="*":
            petition = Request(ip=objetos[1], petition=objetos[2],detection=objetos[3])
            petition.save()
            objetos = []
        else:
            objetos.append(f.rstrip('\n'))

    context = {
        "objetos": objetos, 
    }
    return render(request, "requests.html", context)

    