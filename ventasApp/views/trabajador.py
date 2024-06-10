from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import Trabajador 
from django.db.models import Q 
from ventasApp.forms import TrabajadorForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import datetime

#Funcion para "Gestionar trabajador"
def listartrabajador(request):    
    queryset = request.GET.get("buscar")
    trabajador = Trabajador.objects.all().filter(eliminado=False).order_by('idTrabajador').values()
    if queryset:
        trabajador=Trabajador.objects.filter(Q(apellidos__icontains=queryset)).distinct().filter(eliminado=False).order_by('idTrabajador').values() 
    paginator = Paginator(trabajador, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"trabajador/listar.html",{'page_obj': page_obj})

#Funcion para "Nuevo trabajador"
def agregartrabajador(request):
    if request.method=="POST":
        form=TrabajadorForm(request.POST)
        if form.is_valid():
            email_trabajador = form.cleaned_data.get("email")
            trabajador_exits = (Trabajador.objects.filter(email=email_trabajador).count()>0)
            if trabajador_exits:
                messages.info(request, "Vendedor existente.")
                form=TrabajadorForm(initial={'fechaRegistro':datetime.datetime.now()})
                context={'form':form}
                return render(request,"trabajador/agregar.html",context) 
            else:
                messages.success(request, "Vendedor registrado correctamente.")
                form.save() 
                element = Trabajador.objects.all().last()
                element.usuarioRegistro = request.session['user_logged']
                element.save()
                return redirect("listartrabajador") 

    else:
        form=TrabajadorForm(initial={'fechaRegistro':datetime.datetime.now()})
        context={'form':form} 
        return render(request,"trabajador/agregar.html",context) 

#Funcion para "Editar trabajador"
def editartrabajador(request,id):
    #usuarios_activos = User.objects.filter(is_active=True)
    trabajador=Trabajador.objects.get(idTrabajador=id)
    if request.method=="POST":
        form=TrabajadorForm(request.POST,instance=trabajador)
        if form.is_valid():
            messages.success(request, "Trabajador actualizado.")
            form.save() 
            elemento=Trabajador.objects.get(idTrabajador=id)
            elemento.usuarioModificacion = request.session['user_logged']
            elemento.fechaModificacion = datetime.datetime.now()
            elemento.save()
            return redirect("listartrabajador") 
    else:
        form=TrabajadorForm(instance=trabajador)
        #form.fields['user'].choices = [(u.id, u.username) for u in usuarios_activos]
        context={"form":form} 
        return render(request,"trabajador/edit.html",context)

#Funcion para "Eliminar trabajador"
def eliminartrabajador(request,id):
    trabajador=Trabajador.objects.get(idTrabajador=id) 
    trabajador.activo=False
    trabajador.eliminado=True
    trabajador.usuarioEliminacion = request.session['user_logged']
    trabajador.fechaEliminacion = datetime.datetime.now()
    trabajador.save()
    messages.success(request, "Trabajador eliminado.")
    return redirect("listartrabajador")

def activartrabajador(request,id,activo):
    trabajador=Trabajador.objects.get(idTrabajador=id)
    if activo == 0:
        trabajador.activo=True
    else:
        trabajador.activo=False
    trabajador.save()
    messages.success(request, "Trabajador actualizado.")
    return redirect("listartrabajador") 