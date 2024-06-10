from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import Producto,Categoria 
from django.db.models import Q 
from ventasApp.forms import ProductoForm
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
# Create your views here.
def agregarproducto(request):
    if request.method=="POST":
        form=ProductoForm(request.POST)
        if form.is_valid():
            codigo_producto = form.cleaned_data.get("codigo")
            producto_exits = (Producto.objects.filter(codigo=codigo_producto).count()>0)
            if producto_exits:
                messages.info(request, "Producto ya existe.")
                form=ProductoForm()
                form.fields["categoria"].choices = [(r['idCategoria'],r['descripcion']) for r in Categoria.objects.exclude(eliminado=1).values()]
                context={'form':form}
                return render(request,"producto/agregar.html",context) 
            else:
                messages.success(request, "Producto registrada.")
                form.save() 
                element = Producto.objects.all().last()
                element.usuarioRegistro =  request.session['user_logged']
                if element.nombreImagen != None:
                    element.fechaCargaImagen = datetime.datetime.now()
                element.save()
                return redirect("listarproducto") 

    else:
        cantidad = Producto.objects.count()
        form=ProductoForm(initial={'codigo': str('P-') + str(cantidad+1)})
        form.fields["categoria"].choices = [(r['idCategoria'],r['descripcion']) for r in Categoria.objects.exclude(activo=0).values()]
        context={'form':form} 
        return render(request,"producto/agregar.html",context) 

def listarproducto(request):
    
    queryset = request.GET.get("buscar")
    producto = Producto.objects.all().filter(eliminado=False).order_by('idProducto').values()
    if queryset:
        producto=Producto.objects.filter(Q(codigo__icontains=queryset)).filter(eliminado=False).distinct().order_by('idProducto').values() 
    paginator = Paginator(producto, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'producto':producto}
    return render(request,"producto/listar.html",{'page_obj': page_obj})

def editarproducto(request,id):
    producto=Producto.objects.get(idProducto=id)
    producto_nombreImagen = producto.nombreImagen;
    if request.method=="POST":
        form=ProductoForm(request.POST,instance=producto)
        if form.is_valid():
            messages.success(request, "Producto actualizado.")
            form.save() 
            elemento=Producto.objects.get(idProducto=id)
            elemento.usuarioModificacion = request.session['user_logged']
            elemento.fechaModificacion = datetime.datetime.now()
            if elemento.nombreImagen != producto_nombreImagen:
                elemento.fechaCargaImagen = datetime.datetime.now()
            elemento.save()
            return redirect("listarproducto") 
    else:
        form=ProductoForm(instance=producto)
        form.fields["categoria"].choices = [(r['idCategoria'],r['descripcion']) for r in Categoria.objects.exclude(eliminado=1).values()]
        context={"form":form} 
        return render(request,"producto/edit.html",context)

def eliminarproducto(request,id):
    producto=Producto.objects.get(idProducto=id) 
    producto.activo=False
    producto.eliminado=True
    producto.usuarioEliminacion = request.session['user_logged']
    producto.fechaEliminacion = datetime.datetime.now()
    producto.save()
    messages.success(request, "Producto eliminada.")
    return redirect("listarproducto")

def activarproducto(request,id,activo):
    producto=Producto.objects.get(idProducto=id)
    if activo == 0:
        producto.activo=True
    else:
        producto.activo=False
    producto.save()
    messages.success(request, "Producto actualizada.")
    return redirect("listarproducto") 