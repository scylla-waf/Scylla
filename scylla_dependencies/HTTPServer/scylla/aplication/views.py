from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import ScyllaForm
from .models import Request, Variable

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        Request.objects.all().delete()
        manf = open("scylla_dependencies/WAF/log/petition.log")
        objetos = []
        for f in manf:
            if f.rstrip('\n') == "*":
                if "GET" in " ".join(objetos[2].split(":")[1:])[2:]:
                    petition = Request(ip=objetos[1].split(" ")[1].strip(), petition=" ".join(objetos[2].split(":")[1:])[3:-2].strip(),
                                       detection=objetos[3].split(":")[1].strip(),type_id=objetos[4].split(":")[1].strip())
                else:
                    petition = Request(ip=objetos[1].split(" ")[1].strip(), petition=" ".join(objetos[2].split(":")[1:]).strip(),
                                       detection=objetos[3].split(":")[1].strip(),type_id=objetos[4].split(":")[1].strip())
                petition.save()
                objetos = []
            else:
                objetos.append(f.rstrip('\n'))

        petitions = Request.objects.all()
        page = request.GET.get('page')
        paginator = Paginator(petitions, 10)
        petitions = paginator.get_page(page)
        bad_petitions = Request.objects.all().count()
        manf = open("scylla_dependencies/WAF/log/good.log")
        manf = manf.read().split(",")
        good_petitions = len(manf) - 1
        get_petitions = manf.count("GET")
        post_petitions = manf.count("POST")
        put_petitions = manf.count("PUT")
        if good_petitions == 0:
            other_petitions = 0
        else:
            other_petitions = good_petitions + 1 - (get_petitions + post_petitions + put_petitions)

        context = {
            "petitions": petitions,
            "bad_petitions": bad_petitions,
            "good_petitions": good_petitions,
            "get_petitions": get_petitions,
            "post_petitions": post_petitions,
            "put_petitions": put_petitions,
            "other_petitions": other_petitions,
        }
        return render(request, "index.html", context)
    return redirect('/')

def all(request):
    if request.user.is_authenticated:
        return redirect(request, "index.html", context)
    return redirect('/')

def filter_by_variable_type(request):
    if request.user.is_authenticated:
        petitions = Request.objects.filter(type_id="1")
        page = request.GET.get('page')
        paginator = Paginator(petitions, 10)
        petitions = paginator.get_page(page)

        context = {
            "petitions": petitions,
        }
        return render(request, "index.html", context)
    return redirect('/')


def filter_by_blacklist(request):
    if request.user.is_authenticated:
        petitions = Request.objects.filter(type_id="2")
        page = request.GET.get('page')
        paginator = Paginator(petitions, 10)
        petitions = paginator.get_page(page)

        context = {
            "petitions": petitions,
        }
        return render(request, "index.html", context)
    return redirect('/')

def filter_by_blockip(request):
    if request.user.is_authenticated:
        petitions = Request.objects.filter(type_id="3")
        page = request.GET.get('page')
        paginator = Paginator(petitions, 10)
        petitions = paginator.get_page(page)

        context = {
            "petitions": petitions,
        }
        return render(request, "index.html", context)
    return redirect('/')

def filter_by_method_analysis(request):
    if request.user.is_authenticated:
        petitions = Request.objects.filter(type_id="4")
        page = request.GET.get('page')
        paginator = Paginator(petitions, 10)
        petitions = paginator.get_page(page)

        context = {
            "petitions": petitions,
        }
        return render(request, "index.html", context)
    return redirect('/')

def filter_by_blockbylength(request):
    if request.user.is_authenticated:
        petitions = Request.objects.filter(type_id="5")
        page = request.GET.get('page')
        paginator = Paginator(petitions, 10)
        petitions = paginator.get_page(page)

        context = {
            "petitions": petitions,
        }
        return render(request, "index.html", context)
    return redirect('/')


def config(request):
    manf = open("config/scylla.conf")
    for line in manf:
        if line.split(" ")[0] == "proxyhost":
            proxyhost = line.split(" ")[2]
        elif line.split(" ")[0] == "proxyport":
            proxyport = line.split(" ")[2]
        elif line.split(" ")[0] == "server_addr":
            server_addr = line.split(" ")[2]
        elif line.split(" ")[0] == "server_port":
            server_port = line.split(" ")[2]
        elif line.split(" ")[0] == "HTTPport":
            djangoport = line.split(" ")[2]
        elif line.split(" ")[0] == "secret_key":
            secret_key = line.split(" ")[2]

    formscylla = ScyllaForm(request.POST or None,
                            initial={'proxyhost': proxyhost, 'proxyport': proxyport, 'server_addr': server_addr,
                                     'server_port': server_port, 'djangoport': djangoport,
                                     "secret_key": secret_key[1:-2]})
    if formscylla.is_valid():
        manf = open("config/scylla.conf", "w")
        seq = ["# proxy info ( default in localhost:4440 )\n\n", "proxyhost = " + formscylla.cleaned_data['proxyhost'],
               "\nproxyport = " + formscylla.cleaned_data['proxyport'],
               "\n\n# server info (default)\nserver_addr = " + formscylla.cleaned_data['server_addr'],
               "\nserver_port = " + formscylla.cleaned_data['server_port'], "\n\n# djando info\nsecret_key='",
               formscylla.cleaned_data['secret_key'], "'\nHTTPport = " + formscylla.cleaned_data['djangoport'],
               "\n\n# max bytes received from server\nmaxlength = 10000", ]
        manf.writelines(seq)
        manf.close()
    

    # Miramos los objetos variables para ver los tipos de variable que hay y sus variables


    context = {
        "formscylla": formscylla,
    }
    return render(request, "config.html", context)


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
        if f.rstrip('\n') == "*":
            petition = Request(ip=objetos[1], petition=objetos[2], detection=objetos[3])
            petition.save()
            objetos = []
        else:
            objetos.append(f.rstrip('\n'))

    petitions = Request.objects.all()
    bad_petitions = Request.objects.all().count()
    context = {
        "petitions": petitions,
        "bad_petitions": bad_petitions,
    }
    return render(request, "requests.html", context)
