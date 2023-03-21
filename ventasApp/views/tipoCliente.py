from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import TipoCliente 
from django.db.models import Q 
from ventasApp.forms import TipoClienteForm
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
# Create your views here.
def agregartipoCliente(request):
    if request.method=="POST":
        form=TipoClienteForm(request.POST)
        if form.is_valid():
            descripcion_tipoCliente = form.cleaned_data.get("descripcion")
            tipoCliente_exits = (TipoCliente.objects.filter(descripcion=descripcion_tipoCliente).count()>0)
            if tipoCliente_exits:
                messages.info(request, "TipoCliente ya existe.")
                form=TipoClienteForm()
                context={'form':form}
                return render(request,"tipoCliente/agregar.html",context) 
            else:
                messages.success(request, "TipoCliente registrada.")
                form.save() 
                element = TipoCliente.objects.all().last()
                element.usuarioRegistro =  request.session['user_logged']
                element.save()
                return redirect("listartipoCliente") 

    else:
        form=TipoClienteForm()
        context={'form':form} 
        return render(request,"tipoCliente/agregar.html",context) 

def listartipoCliente(request):
    
    queryset = request.GET.get("buscar")
    tipoCliente = TipoCliente.objects.all().filter(eliminado=False).order_by('-idTipoCliente').values()
    if queryset:
        tipoCliente=TipoCliente.objects.filter(Q(descripcion__icontains=queryset)).filter(eliminado=False).distinct().order_by('-idTipoCliente').values() 
    paginator = Paginator(tipoCliente, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'tipoCliente':tipoCliente}
    return render(request,"tipoCliente/listar.html",{'page_obj': page_obj})

def editartipoCliente(request,id):
    tipoCliente=TipoCliente.objects.get(idTipoCliente=id)
    if request.method=="POST":
        form=TipoClienteForm(request.POST,instance=tipoCliente)
        if form.is_valid():
            messages.success(request, "Cliente actualizado.")
            form.save() 
            elemento=TipoCliente.objects.get(idTipoCliente=id)
            elemento.usuarioModificacion = request.session['user_logged']
            elemento.fechaModificacion = datetime.datetime.now()
            elemento.save()
            return redirect("listartipoCliente") 
    else:
        form=TipoClienteForm(instance=tipoCliente)
        context={"form":form} 
        return render(request,"tipoCliente/edit.html",context)

def eliminartipoCliente(request,id):
    tipoCliente=TipoCliente.objects.get(idTipoCliente=id) 
    tipoCliente.activo=False
    tipoCliente.eliminado=True
    tipoCliente.usuarioEliminacion = request.session['user_logged']
    tipoCliente.fechaEliminacion = datetime.datetime.now()
    tipoCliente.save()
    messages.success(request, "TipoCliente eliminada.")
    return redirect("listartipoCliente")

def activartipoCliente(request,id,activo):
    tipoCliente=TipoCliente.objects.get(idTipoCliente=id)
    if activo == 0:
        tipoCliente.activo=True
    else:
        tipoCliente.activo=False
    tipoCliente.save()
    messages.success(request, "TipoCliente actualizada.")
    return redirect("listartipoCliente") 