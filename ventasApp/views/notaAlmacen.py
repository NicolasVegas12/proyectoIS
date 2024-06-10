from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import *
from django.db.models import Q 
from ventasApp.forms import NotaAlmacenForm
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.
def agregarnotaAlmacen(request):
    if request.method=="POST":
        form=NotaAlmacenForm(request.POST)
        messages.success(request, "Nota de Almacén registrada.")
        form.save() 
        element = NotaAlmacen.objects.all().last()

        if (form['pedidoVenta'].value() != None) and form['pedidoVenta'].value() != '':            
            pedidoVenta_exits = PedidoVenta.objects.get(idPedidoVenta=form['pedidoVenta'].value())
            #pedidoVenta_exits = PedidoVenta.objects.filter(idPedidoVenta=form['pedidoVenta'].value())
            detallePedidoVenta = DetallePedidoVenta.objects.all().filter(pedidoVenta=pedidoVenta_exits).values()
            for p in detallePedidoVenta:                
                Vproducto = Producto.objects.get(idProducto=int(p['producto_id']))
                detalle = DetalleNotaAlmacen(
                    notaAlmacen= element,
                    producto= Vproducto,
                    cantidad=p['cantidad'],
                    precioUnitario=p['precioUnitario'],
                    descuentoUnitario=p['descuentoUnitario'],
                    precio=p['precio'],
                    usuarioRegistro = request.session['user_logged'],
                    cantidadTotal = int(Vproducto.stock),
                    cantidadUsada = int(p['cantidad']),
                    cantidadSaldo = int(Vproducto.stock) -int(p['cantidad']),
                )
                Vproducto.stock = int(Vproducto.stock) -int(p['cantidad'])
                Vproducto.save()
                detalle.save()
                
        if (form['ordenCompra'].value() != None) and form['ordenCompra'].value() != '':
            
            ordenCompra_exits = OrdenCompra.objects.get(idOrdenCompra=form['ordenCompra'].value())
            detalleOrdenCompra = DetalleOrdenCompra.objects.all().filter(ordenCompra=ordenCompra_exits).values()

            for p in detalleOrdenCompra:
                
                Vproducto = Producto.objects.get(idProducto=int(p['producto_id']))
                detalle = DetalleNotaAlmacen(
                    notaAlmacen= element,
                    producto= Vproducto,
                    cantidad=p['cantidad'],
                    precioUnitario=p['precioUnitario'],
                    descuentoUnitario=p['descuentoUnitario'],
                    precio=p['precio'],
                    usuarioRegistro = request.session['user_logged'],
                    cantidadTotal = int(Vproducto.stock),
                    cantidadUsada = int(p['cantidad']),
                    cantidadSaldo = int(Vproducto.stock) + int(p['cantidad']),
                )
                Vproducto.stock = int(Vproducto.stock) + int(p['cantidad'])
                Vproducto.save()
                detalle.save()
        
        return redirect("listarnotaAlmacen")
    
    else:
        cantidad = NotaAlmacen.objects.count()
        form=NotaAlmacenForm(initial={'fechaEmision':datetime.datetime.now().strftime("%Y-%m-%d"),'fechaEntrega':datetime.datetime.now().strftime("%Y-%m-%d"),'codigo': str('NT-') + str(cantidad+1)})
        context={'form':form} 
        return render(request,"notaAlmacen/agregar.html",context) 

def listarnotaAlmacen(request):
    queryset = request.GET.get("buscar")
    notaAlmacen = NotaAlmacen.objects.all().filter(eliminado=False).order_by('-idNotaAlmacen').values()
    if queryset:
        notaAlmacen=NotaAlmacen.objects.filter(Q(codigo__icontains=queryset)).filter(eliminado=False).distinct().order_by('-idNotaAlmacen').values() 
    paginator = Paginator(notaAlmacen, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'notaAlmacen':notaAlmacen}
    return render(request,"notaAlmacen/listar.html",{'page_obj': page_obj})

def editarnotaAlmacen(request,id):
    notaAlmacen=NotaAlmacen.objects.get(idNotaAlmacen=id)
    if request.method=="POST":
        form=NotaAlmacenForm(request.POST,instance=notaAlmacen)
        if form.is_valid():
            messages.success(request, "Orden actualizada.")
            form.save() 
            return redirect("listarnotaAlmacen") 
    else:
        form=NotaAlmacenForm(instance=notaAlmacen)
        pedidoVenta_exits = (PedidoVenta.objects.filter(idPedidoVenta=notaAlmacen.pedidoVenta_id).count()>0)
        if pedidoVenta_exits:
            pedidoVenta=PedidoVenta.objects.get(idPedidoVenta=notaAlmacen.pedidoVenta_id)
            confirmacion = True
            context={"form":form,'id':pedidoVenta.idPedidoVenta, 'confirmacion':confirmacion} 
        else :
            ordenCompra=OrdenCompra.objects.get(idOrdenCompra=notaAlmacen.ordenCompra_id) 
            confirmacion = False
            context={"form":form,'id':ordenCompra.idOrdenCompra, 'confirmacion':confirmacion}
        return render(request,"notaAlmacen/edit.html",context)

def eliminarnotaAlmacen(request,id):
    notaAlmacen=NotaAlmacen.objects.get(idNotaAlmacen=id) 
    notaAlmacen.activo=False
    notaAlmacen.eliminado=True
    notaAlmacen.save()
    messages.success(request, "Nota de Almacén eliminada.")
    return redirect("listarnotaAlmacen")

def activarnotaAlmacen(request,id,activo):
    notaAlmacen=NotaAlmacen.objects.get(idNotaAlmacen=id)
    if activo == 0:
        notaAlmacen.activo=True
    else:
        notaAlmacen.activo=False
    notaAlmacen.save()
    messages.success(request, "Nota de Almacén actualizada.")
    return redirect("listarnotaAlmacen") 