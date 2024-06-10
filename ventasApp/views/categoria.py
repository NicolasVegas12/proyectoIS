from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import Categoria 
from django.db.models import Q 
from ventasApp.forms import CategoriaForm
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
# Create your views here.
def agregarcategoria(request):
    if request.method=="POST":
        form=CategoriaForm(request.POST)
        if form.is_valid():
            descripcion_categoria = form.cleaned_data.get("descripcion")
            categoria_exits = (Categoria.objects.filter(descripcion=descripcion_categoria).count()>0)
            if categoria_exits:
                messages.info(request, "Categoria ya existe.")
                form=CategoriaForm()
                context={'form':form}
                return render(request,"categoria/agregar.html",context) 
            else:
                messages.success(request, "Categoria registrada.")
                form.save() 
                element = Categoria.objects.all().last()
                element.usuarioRegistro =  request.session['user_logged']
                element.save()
                return redirect("listarcategoria")                 
    else:
        form=CategoriaForm()
        context={'form':form} 
        return render(request,"categoria/agregar.html",context) 

def listarcategoria(request):    
    queryset = request.GET.get("buscar")
    categoria = Categoria.objects.all().filter(eliminado=False).order_by('idCategoria').values()
    if queryset:
        categoria=Categoria.objects.filter(Q(descripcion__icontains=queryset)).filter(eliminado=False).distinct().order_by('idCategoria').values() 
    paginator = Paginator(categoria, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'categoria':categoria}
    return render(request,"categoria/listar.html",{'page_obj': page_obj})

def editarcategoria(request,id):
    categoria=Categoria.objects.get(idCategoria=id)
    if request.method=="POST":
        form=CategoriaForm(request.POST,instance=categoria)
        if form.is_valid():
            messages.success(request, "Categoria actualizada.")
            form.usuarioModificacion = request.session['user_logged']
            form.save() 
            elemento=Categoria.objects.get(idCategoria=id)
            elemento.usuarioModificacion = request.session['user_logged']
            elemento.fechaModificacion = datetime.datetime.now()
            elemento.save()
            return redirect("listarcategoria") 
    else:
        form=CategoriaForm(instance=categoria)
        context={"form":form} 
        return render(request,"categoria/edit.html",context)

def eliminarcategoria(request,id):
    categoria=Categoria.objects.get(idCategoria=id) 
    categoria.activo=False
    categoria.eliminado=True
    categoria.usuarioEliminacion = request.session['user_logged']
    categoria.fechaEliminacion = datetime.datetime.now()
    categoria.save()
    messages.success(request, "Categoria eliminada.")
    return redirect("listarcategoria")

def activarcategoria(request,id,activo):
    categoria=Categoria.objects.get(idCategoria=id)
    if activo == 0:
        categoria.activo=True
    else:
        categoria.activo=False
    categoria.save()
    messages.success(request, "Categoria actualizada.")
    return redirect("listarcategoria") 