from wsgiref.validate import validator
from django.forms import Form
from django.shortcuts import render, redirect
from typing import Generic
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,Permission,Group
from django.core.paginator import Paginator
from django.db.models import Q 
from ventasApp.forms import UsuarioForm,UsuarioEditForm



def listarpermiso(request):    
    queryset = request.GET.get("buscar")
    permiso = Permission.objects.all().order_by('id').values()
    if queryset:
        permiso = Permission.objects.filter(Q(name__icontains=queryset)).distinct().order_by('id').values() 
    paginator = Paginator(permiso, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"permiso/listar.html",{'page_obj': page_obj})
