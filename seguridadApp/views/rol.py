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
from ventasApp.forms import GroupForm


def listarrole(request):    
    queryset = request.GET.get("buscar")
    role = Group.objects.all().order_by('id').values()
    if queryset:
        role = Group.objects.filter(Q(name__icontains=queryset)).distinct().order_by('id').values() 
    paginator = Paginator(role,3)
    page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    return render(request,"role/listar.html",{'roles': role})

def agregarrole(request):
    if request.method=="POST":
        form=GroupForm(request.POST)
        if form.is_valid():
            role_role = form.cleaned_data.get("name")
            role_exits = (Group.objects.filter(name=role_role).count()>0)
            if role_exits:
                messages.info(request, "El Rol ya existe.")
                form=GroupForm()
                context={'form':form}
                return render(request,"role/agregar.html",context) 
            else:
                messages.success(request, "Usuario registrado.")
                Group.objects.get_or_create(name=form.cleaned_data.get("name"))
                return redirect("listarrole") 

    else:
        form=GroupForm()
        context={'form':form} 
        return render(request,"role/agregar.html",context)

def editarrole(request,id):
    role=Group.objects.get(id=id)
    if request.method=="POST":
        form=GroupForm(request.POST)
        if form.is_valid():
            role.name = form.cleaned_data.get("name")
            role.save()
            messages.success(request, "Rol actualizado.")
            return redirect("listarrole") 
    else:
        initial_dict = {
            "name":role.name,
        }
        form=GroupForm(initial=initial_dict)
        context={"form":form} 
        return render(request,"role/editar.html",context)

def eliminarrole(request,id):
    Group.objects.get(id=id).delete() 
    messages.success(request, "Rol eliminado.")
    return redirect("listarrole")