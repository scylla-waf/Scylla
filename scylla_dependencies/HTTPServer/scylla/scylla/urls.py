"""scylla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from aplication import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout_view),
    path('index.html', views.index),
    path('config', views.config),
    path('filter_by_variable_type', views.filter_by_variable_type),
    path('filter_by_blacklist', views.filter_by_blacklist),
    path('filter_by_blockip', views.filter_by_blockip),
    path('filter_by_method_analysis', views.filter_by_method_analysis),
    path('filter_by_blockbylength', views.filter_by_blockbylength),
    path('all', views.index),
    
]
