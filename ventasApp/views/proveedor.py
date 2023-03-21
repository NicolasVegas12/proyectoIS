from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import Proveedor 
from django.db.models import Q 
from ventasApp.forms import ProveedorForm
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
# Create your views here.
def agregarproveedor(request):
    if request.method=="POST":
        form=ProveedorForm(request.POST)
        if form.is_valid():
            ruc_proveedor = form.cleaned_data.get("ruc")
            proveedor_exits = (Proveedor.objects.filter(ruc=ruc_proveedor).count()>0)
            if proveedor_exits:
                messages.info(request, "Proveedor ya existe.")
                form=ProveedorForm()
                context={'form':form}
                return render(request,"proveedor/agregar.html",context) 
            else:
                messages.success(request, "Proveedor registrada.")
                form.save() 
                element = Proveedor.objects.all().last()
                element.usuarioRegistro =  request.session['user_logged']
                element.save()
                return redirect("listarproveedor") 

    else:
        form=ProveedorForm()
        context={'form':form} 
        return render(request,"proveedor/agregar.html",context) 

def listarproveedor(request):
    
    queryset = request.GET.get("buscar")
    proveedor = Proveedor.objects.all().filter(eliminado=False).order_by('-idProveedor').values()
    if queryset:
        proveedor=Proveedor.objects.filter(Q(ruc__icontains=queryset)).filter(eliminado=False).distinct().order_by('-idProveedor').values() 
    paginator = Paginator(proveedor, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'proveedor':proveedor}
    return render(request,"proveedor/listar.html",{'page_obj': page_obj})

def editarproveedor(request,id):
    proveedor=Proveedor.objects.get(idProveedor=id)
    if request.method=="POST":
        form=ProveedorForm(request.POST,instance=proveedor)
        if form.is_valid():
            messages.success(request, "Proveedor actualizada.")
            form.save() 
            elemento = Proveedor.objects.get(idProveedor=id)
            elemento.usuarioModificacion = request.session['user_logged']
            elemento.fechaModificacion = datetime.datetime.now()
            elemento.save()
            return redirect("listarproveedor") 
    else:
        form=ProveedorForm(instance=proveedor)
        context={"form":form} 
        return render(request,"proveedor/edit.html",context)

def eliminarproveedor(request,id):
    proveedor=Proveedor.objects.get(idProveedor=id) 
    proveedor.activo=False
    proveedor.eliminado=True
    proveedor.usuarioEliminacion = request.session['user_logged']
    proveedor.fechaEliminacion = datetime.datetime.now()
    proveedor.save()
    messages.success(request, "Proveedor eliminada.")
    return redirect("listarproveedor")

def activarproveedor(request,id,activo):
    proveedor=Proveedor.objects.get(idProveedor=id)
    if activo == 0:
        proveedor.activo=True
    else:
        proveedor.activo=False
    proveedor.save()
    messages.success(request, "Proveedor actualizada.")
    return redirect("listarproveedor") 