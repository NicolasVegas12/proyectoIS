from django.http import HttpResponse
from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import * 
from django.db.models import Q 
from ventasApp.forms import OrdenCompraForm
from django.contrib import messages
from django.core.paginator import Paginator
from ventasApp.utils import render_to_pdf
# Create your views here.
def agregarordenCompra(request):
    list_product = Producto.objects.all().filter(activo=True).values()
    if request.method=="POST":
        form=OrdenCompraForm(request.POST)

        arregloObjetoProductos = []  
        ordenCompra_subtotal = 0.0
        ordenCompra_descuento = 0.0
        ordenCompra_total = 0.0

        idProducto = request.POST.getlist('idProducto[]')
        idCantidad = request.POST.getlist('idCantidad[]')
        idPrecioUnitario = request.POST.getlist('idPrecioUnitario[]')
        idDescuentoUnitario = request.POST.getlist('idDescuentoUnitario[]')
        idPrecioProductoTotal = request.POST.getlist('idPrecioProductoTotal[]')
        i=0
        
        while i<len(idProducto):
            ordenCompra_subtotal = ordenCompra_subtotal+(float(idCantidad[i])*float(idPrecioUnitario[i]))
            ordenCompra_descuento = ordenCompra_descuento+float(idDescuentoUnitario[i])
            ordenCompra_total = ordenCompra_total+float(idPrecioProductoTotal[i])

            arregloObjetoProductos.append({
                'Producto':idProducto[i],
                'Cantidad':idCantidad[i],
                'PrecioUnitario':idPrecioUnitario[i],
                'DescuentoUnitario':idDescuentoUnitario[i],
                'PrecioProductoTotal':idPrecioProductoTotal[i],
            })
            i+=1
        
        ordenCompra = OrdenCompra.objects.create(                     
                        trabajador = Trabajador.objects.get(idTrabajador=form['trabajador'].value()),
                        proveedor = Proveedor.objects.get(idProveedor=form['proveedor'].value()),
                        formaPago = FormaPago.objects.get(idFormaPago=form['formaPago'].value()),
                        codigo = form['codigo'].value(),
                        fechaEmision = form['fechaEmision'].value(),
                        fechaEntrega = form['fechaEntrega'].value(),
                        tipoMoneda = form['tipoMoneda'].value(),
                        tasaCambio = form['tasaCambio'].value(),
                        
                        tasaIgv = form['tasaIgv'].value(),
                        estado = form['estado'].value(),

                        subtotal = ordenCompra_subtotal,
                        descuento = ordenCompra_descuento,
                        total = ordenCompra_total,
                        tipoDocumento = form['tipoDocumento'].value(),
                        usuarioRegistro = request.session['user_logged']
                    )
        ordenCompra.save()
        element = OrdenCompra.objects.all().last()
        cantidadD = OrdenCompra.objects.count()
        documentoOrdenCompra = DocumentoCompra.objects.create(
                        ordenCompra = element,
                        serie = '00',
                        numero = str(cantidadD+1),
                        tipoDocumento = form['tipoDocumento'].value(),
                        usuarioRegistro = request.session['user_logged']
                    )
        documentoOrdenCompra.save()
        for p in arregloObjetoProductos:
            detalle = DetalleOrdenCompra(
                ordenCompra = element,
                producto= Producto.objects.get(idProducto=p['Producto']), 
                cantidad=p['Cantidad'],
                precioUnitario=p['PrecioUnitario'],
                descuentoUnitario=p['DescuentoUnitario'],
                precio=p['PrecioProductoTotal'],
                usuarioRegistro = request.session['user_logged']
            )
            detalle.save()
        messages.success(request, "Orden de Compra registrada.")
        return redirect("listarordenCompra") 
    
    else:
        cantidad = OrdenCompra.objects.count()
        form=OrdenCompraForm(initial={'fechaEmision':datetime.datetime.now().strftime("%Y-%m-%d"),'fechaEntrega':datetime.datetime.now().strftime("%Y-%m-%d"),'tasaIgv': 0.18,'tasaCambio': 0,'codigo': str('OC-') + str(cantidad+1)})
        form.fields["proveedor"].choices = [(r['idProveedor'],str(r['nombreComercial']) +' || '+ str(r['ruc'])) for r in Proveedor.objects.filter(activo=True).values()]
        context={'form':form,'list_product':list_product} 
        return render(request,"ordenCompra/agregar.html",context) 

def listarordenCompra(request):
    queryset = request.GET.get("buscar")
    ordenCompra = OrdenCompra.objects.all().filter(eliminado=False).order_by('-idOrdenCompra').values()
    if queryset:
        ordenCompra=OrdenCompra.objects.filter(Q(codigo__icontains=queryset)).filter(eliminado=False).distinct().order_by('-idOrdenCompra').values() 
    paginator = Paginator(ordenCompra, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'ordenCompra':ordenCompra}
    return render(request,"ordenCompra/listar.html",{'page_obj': page_obj})

def editarordenCompra(request,id):
    list_product = Producto.objects.all().filter(eliminado=False).values()
    ordenCompra=OrdenCompra.objects.get(idOrdenCompra=id)
    if request.method=="POST":
        form=OrdenCompraForm(request.POST)

        arregloObjetoProductos = []  
        ordenCompra_subtotal = 0.0
        ordenCompra_descuento = 0.0
        ordenCompra_total = 0.0

        arregloProductosEliminados = [] 
        idDetalleEliminado = request.POST.getlist('idDetalleEliminado[]')
        idDetalle = request.POST.getlist('idDetalle[]')
        idProducto = request.POST.getlist('idProducto[]')
        idCantidad = request.POST.getlist('idCantidad[]')
        idPrecioUnitario = request.POST.getlist('idPrecioUnitario[]')
        idDescuentoUnitario = request.POST.getlist('idDescuentoUnitario[]')
        idPrecioProductoTotal = request.POST.getlist('idPrecioProductoTotal[]')
        j=0
        while(j<len(idDetalleEliminado)):
            arregloProductosEliminados.append({
                'Detalle':idDetalleEliminado[j]
            })
            j+=1

        i=0
        while i<len(idProducto):
            ordenCompra_subtotal = ordenCompra_subtotal+(float(idCantidad[i])*float(idPrecioUnitario[i]))
            ordenCompra_descuento = ordenCompra_descuento+float(idDescuentoUnitario[i])
            ordenCompra_total = ordenCompra_total+float(idPrecioProductoTotal[i])

            arregloObjetoProductos.append({
                'Detalle':idDetalle[i],
                'Producto':idProducto[i],
                'Cantidad':idCantidad[i],
                'PrecioUnitario':idPrecioUnitario[i],
                'DescuentoUnitario':idDescuentoUnitario[i],
                'PrecioProductoTotal':idPrecioProductoTotal[i],
            })
            i+=1

        for z in arregloProductosEliminados:
            detalle = DetalleOrdenCompra.objects.get(idDetalleOrdenCompra=z['Detalle'])
            detalle.usuarioEliminacion = request.session['user_logged']
            detalle.fechaEliminacion = datetime.datetime.now()
            detalle.eliminado = True
            detalle.save()

        for p in arregloObjetoProductos:
            if p['Detalle'] == 0:
                detalle = DetalleOrdenCompra(
                    ordenCompra = ordenCompra,
                    producto= Producto.objects.get(idProducto=p['Producto']), 
                    cantidad=p['Cantidad'],
                    precioUnitario=p['PrecioUnitario'],
                    descuentoUnitario=p['DescuentoUnitario'],
                    precio=p['PrecioProductoTotal'],
                    usuarioRegistro = request.session['user_logged']
                )
                detalle.save()
            else:
                detalle = DetalleOrdenCompra.objects.get(idDetalleOrdenCompra=p['Detalle'])
                detalle.cantidad=p['Cantidad']
                detalle.precioUnitario=p['PrecioUnitario']
                detalle.descuentoUnitario=p['DescuentoUnitario']
                detalle.precio=p['PrecioProductoTotal']
                detalle.usuarioModificacion = request.session['user_logged']
                detalle.fechaModificacion = datetime.datetime.now()
                detalle.save()
        
        ordenCompra.trabajador = Trabajador.objects.get(idTrabajador=form['trabajador'].value())
        ordenCompra.proveedor = Proveedor.objects.get(idProveedor=form['proveedor'].value())
        ordenCompra.formaPago = FormaPago.objects.get(idFormaPago=form['formaPago'].value())
        ordenCompra.fechaEmision = form['fechaEmision'].value()
        ordenCompra.fechaEntrega =  form['fechaEntrega'].value()
        ordenCompra.tipoMoneda = form['tipoMoneda'].value()
        ordenCompra.tasaCambio = form['tasaCambio'].value()
        ordenCompra.tasaIgv = form['tasaIgv'].value()
        ordenCompra.estado = form['estado'].value()
        ordenCompra.tipoDocumento = form['tipoDocumento'].value()
        ordenCompra.subtotal = ordenCompra_subtotal
        ordenCompra.descuento = ordenCompra_descuento
        ordenCompra.total = ordenCompra_total
        
        ordenCompra.usuarioModificacion = request.session['user_logged']
        ordenCompra.fechaModificacion = datetime.datetime.now()
        ordenCompra.save()
        documento = DocumentoCompra.objects.get(ordenCompra=ordenCompra)
        documento.tipoDocumento = form['tipoDocumento'].value()
        documento.save()
        messages.success(request, "Orden de compra actualizada.")
        
        return redirect("listarordenCompra")  
    else:
        form=OrdenCompraForm(instance=ordenCompra)
        form.fields["proveedor"].choices = [(r['idProveedor'],str(r['ruc']) +' '+str(r['razonSocial'])) for r in Proveedor.objects.exclude(eliminado=1).values()]
        context={"form":form,'list_product':list_product,'ordenCompra':ordenCompra,'id':id} 
        return render(request,"ordenCompra/edit.html",context)

def eliminarordenCompra(request,id):
    ordenCompra=OrdenCompra.objects.get(idOrdenCompra=id) 
    ordenCompra.activo=False
    ordenCompra.eliminado=True
    ordenCompra.save()
    messages.success(request, "Orden de compra eliminada.")
    return redirect("listarordenCompra")

def activarordenCompra(request,id,activo):
    ordenCompra=OrdenCompra.objects.get(idOrdenCompra=id)
    if activo == 0:
        ordenCompra.activo=True
    else:
        ordenCompra.activo=False
    ordenCompra.save()
    messages.success(request, "Orden de compra actualizada.")
    return redirect("listarordenCompra") 

def ListOrdenCompraPdf(View, id):
    ordenCompra = OrdenCompra.objects.get(idOrdenCompra=id)
    proveedor = Proveedor.objects.get(idProveedor=ordenCompra.proveedor_id)
    detalle = DetalleOrdenCompra.objects.all().filter(ordenCompra=id).filter(eliminado=False).values()
    producto= DetalleOrdenCompra.objects.select_related('Producto')
    documento = DocumentoCompra.objects.get(ordenCompra=id)
    data = {
        'proveedor':proveedor,
        'ordenCompra': ordenCompra,
        'documento':documento,
        'detalle': detalle,
        'productos':producto
    }
    pdf = render_to_pdf('ordenCompra/listview.html', data)
    return HttpResponse(pdf, content_type='application/pdf')