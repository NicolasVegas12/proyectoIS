import qrcode
import base64
from io import BytesIO
from django.template.loader import render_to_string

from django.http import HttpResponse
from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import *
from django.db.models import Q 
from ventasApp.forms import PedidoVentaForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView, View
from django.http import JsonResponse
from ventasApp.utils import render_to_pdf
# Create your views here.
def agregarpedidoVenta(request):
    list_product = Producto.objects.all().filter(activo=True).values()
    if request.method=="POST":
        form=PedidoVentaForm(request.POST)

        arregloObjetoProductos = []  
        pedidoVenta_subtotal = 0.0
        pedidoVenta_descuento = 0.0
        pedidoVenta_total = 0.0

        idProducto = request.POST.getlist('idProducto[]')
        idCantidad = request.POST.getlist('idCantidad[]')
        idPrecioUnitario = request.POST.getlist('idPrecioUnitario[]')
        idDescuentoUnitario = request.POST.getlist('idDescuentoUnitario[]')
        idPrecioProductoTotal = request.POST.getlist('idPrecioProductoTotal[]')
        i=0

        #Crea una lista de Productos en el Pedido
        while i<len(idProducto):
            pedidoVenta_subtotal = pedidoVenta_subtotal+(float(idCantidad[i])*float(idPrecioUnitario[i]))
            pedidoVenta_descuento = pedidoVenta_descuento+float(idDescuentoUnitario[i])
            pedidoVenta_total = pedidoVenta_total+float(idPrecioProductoTotal[i])

            arregloObjetoProductos.append({
                'Producto':idProducto[i],
                'Cantidad':idCantidad[i],
                'PrecioUnitario':idPrecioUnitario[i],
                'DescuentoUnitario':idDescuentoUnitario[i],
                'PrecioProductoTotal':idPrecioProductoTotal[i],
            })
            i+=1
        

        
        for p in arregloObjetoProductos:
            producto_id = p['Producto']
            cantidad = p['Cantidad']

            # Retrieve the product from the database
            product = Producto.objects.get(idProducto=producto_id)

            # Check if the entered quantity exceeds the available stock
            if int(cantidad) > product.stock and int(cantidad) < 0:
                print("Cantidad no valida: La cantidad ingresada para el producto {} excede el stock disponible.".format(product.nombre))
                messages.error(request, "Ocurrio algun error en el registro")
                return redirect("agregarpedidoVenta")
            else:
                pedidoVenta = PedidoVenta.objects.create(
                        trabajador = Trabajador.objects.get(idTrabajador=form['trabajador'].value()),

                        #trabajador = Trabajador.objects.filter(eliminado=False).value(),
                        cliente = Cliente.objects.get(idCliente=form['cliente'].value()),
                        formaPago = FormaPago.objects.get(idFormaPago=form['formaPago'].value()),
                        codigo = form['codigo'].value(),
                        fechaEmision = form['fechaEmision'].value(),
                        fechaEntrega = form['fechaEntrega'].value(),
                        tipoMoneda = form['tipoMoneda'].value(),
                        tasaCambio = form['tasaCambio'].value(),
                        
                        tasaIgv = form['tasaIgv'].value(),
                        estado = form['estado'].value(),

                        subtotal = pedidoVenta_subtotal,
                        descuento = pedidoVenta_descuento,
                        total = pedidoVenta_total,
                        tipoDocumento = form['tipoDocumento'].value(),
                        usuarioRegistro = request.session['user_logged']
                    )
        
                pedidoVenta.save()

                #Creando Documento de venta
                element = PedidoVenta.objects.all().last()
                cantidadD = PedidoVenta.objects.count()        
                documentoPedidoVenta = DocumentoVenta.objects.create(
                                pedidoVenta = element,
                                codigo = str('DOC-') + str(cantidadD+1),
                                serie = '00',
                                numero = str(cantidadD+1),
                                tipoDocumento = form['tipoDocumento'].value(),
                                usuarioRegistro = request.session['user_logged']
                            )
                documentoPedidoVenta.save()

                
                
                
                detalle = DetallePedidoVenta(
                        pedidoVenta=element,
                        producto=product,
                        cantidad=cantidad,
                        precioUnitario=p['PrecioUnitario'],
                        descuentoUnitario=p['DescuentoUnitario'],
                        precio=p['PrecioProductoTotal'],
                        usuarioRegistro=request.session['user_logged']
                    )  
                detalle.save()
                messages.success(request, "Pedido de Venta registrada.")

                #product.stock -= int(cantidad)
                #product.save()

        return redirect("listarpedidoVenta")
      
    
    else:
        cantidad = PedidoVenta.objects.count()
        form=PedidoVentaForm(initial={'fechaEmision':datetime.datetime.now().strftime("%Y-%m-%d"),'fechaEntrega':datetime.datetime.now().strftime("%Y-%m-%d"),'tasaIgv': 0.18,'tasaCambio': 0,'codigo': str('PV-') + str(cantidad+1)})
        form.fields["cliente"].choices = [(r['idCliente'],str(r['apellidos']) +' '+ str(r['nombres'])) for r in Cliente.objects.filter(activo=True).values()]
        context={'form':form,'list_product':list_product} 
        return render(request,"pedidoVenta/agregar.html",context) 

def listarpedidoVenta(request):
    queryset = request.GET.get("buscar")
    pedidoVenta = PedidoVenta.objects.all().order_by('-idPedidoVenta').values()
    if queryset:
        pedidoVenta=PedidoVenta.objects.filter(Q(codigo__icontains=queryset)).distinct().order_by('-idPedidoVenta').values() 
    paginator = Paginator(pedidoVenta, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"pedidoVenta/listar.html",{'page_obj': page_obj})

def editarpedidoVenta(request,id):
    list_product = Producto.objects.all().filter(eliminado=False).values()
    pedidoVenta=PedidoVenta.objects.get(idPedidoVenta=id)
    if request.method=="POST":
        form=PedidoVentaForm(request.POST)

        arregloObjetoProductos = []  
        pedidoVenta_subtotal = 0.0
        pedidoVenta_descuento = 0.0
        pedidoVenta_total = 0.0

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
            pedidoVenta_subtotal = pedidoVenta_subtotal+(float(idCantidad[i])*float(idPrecioUnitario[i]))
            pedidoVenta_descuento = pedidoVenta_descuento+float(idDescuentoUnitario[i])
            pedidoVenta_total = pedidoVenta_total+float(idPrecioProductoTotal[i])

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
            detalle = DetallePedidoVenta.objects.get(idDetallePedidoVenta=z['Detalle'])
            detalle.usuarioEliminacion = request.session['user_logged']
            detalle.fechaEliminacion = datetime.datetime.now()
            detalle.eliminado = True
            detalle.save()

        for p in arregloObjetoProductos:
            if p['Detalle'] == 0:
                detalle = DetallePedidoVenta(
                    pedidoVenta = pedidoVenta,
                    producto= Producto.objects.get(idProducto=p['Producto']), 
                    cantidad=p['Cantidad'],
                    precioUnitario=p['PrecioUnitario'],
                    descuentoUnitario=p['DescuentoUnitario'],
                    precio=p['PrecioProductoTotal'],
                    usuarioRegistro = request.session['user_logged']
                )
                detalle.save()
            else:
                detalle = DetallePedidoVenta.objects.get(idDetallePedidoVenta=p['Detalle'])
                detalle.cantidad=p['Cantidad']
                detalle.precioUnitario=p['PrecioUnitario']
                detalle.descuentoUnitario=p['DescuentoUnitario']
                detalle.precio=p['PrecioProductoTotal']
                detalle.usuarioModificacion = request.session['user_logged']
                detalle.fechaModificacion = datetime.datetime.now()
                detalle.save()
        
        pedidoVenta.trabajador = Trabajador.objects.get(idTrabajador=form['trabajador'].value())
        pedidoVenta.cliente = Cliente.objects.get(idCliente=form['cliente'].value())
        pedidoVenta.formaPago = FormaPago.objects.get(idFormaPago=form['formaPago'].value())
        pedidoVenta.fechaEmision = form['fechaEmision'].value()
        pedidoVenta.fechaEntrega =  form['fechaEntrega'].value()
        pedidoVenta.tipoMoneda = form['tipoMoneda'].value()
        pedidoVenta.tasaCambio = form['tasaCambio'].value()
        pedidoVenta.tasaIgv = form['tasaIgv'].value()
        pedidoVenta.estado = form['estado'].value()
        pedidoVenta.tipoDocumento = form['tipoDocumento'].value()
        pedidoVenta.subtotal = pedidoVenta_subtotal
        pedidoVenta.descuento = pedidoVenta_descuento
        pedidoVenta.total = pedidoVenta_total
        
        pedidoVenta.usuarioModificacion = request.session['user_logged']
        pedidoVenta.fechaModificacion = datetime.datetime.now()
        pedidoVenta.save()
        documento = DocumentoVenta.objects.get(pedidoVenta=pedidoVenta)
        documento.tipoDocumento = form['tipoDocumento'].value()
        documento.save()
        messages.success(request, "Pedido de Venta actualizada.")
        
        return redirect("listarpedidoVenta")  
    else:
        form=PedidoVentaForm(instance=pedidoVenta)
        form.fields["cliente"].choices = [(r['idCliente'],str(r['apellidos']) +' '+str(r['nombres'])) for r in Cliente.objects.exclude(eliminado=1).values()]
        context={"form":form,'list_product':list_product,'pedidoVenta':pedidoVenta,'id':id} 
        return render(request,"pedidoVenta/edit.html",context)

def eliminarpedidoVenta(request,id):
    pedidoVenta=PedidoVenta.objects.get(idPedidoVenta=id) 
    pedidoVenta.eliminado=True
    pedidoVenta.estado=3
    pedidoVenta.usuarioEliminacion = request.session['user_logged']
    pedidoVenta.fechaEliminacion = datetime.datetime.now()
    pedidoVenta.save()
    messages.success(request, "Pedido de venta eliminado.")
    return redirect("listarpedidoVenta")

from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

def render_to_pdf(template_path, context_dict, filename):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, show_error_as_pdf=True, encoding='UTF-8')
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', content_type='text/plain')

    return response



def ListPedidoVentaPdf(View, id):
    pedidoVenta = PedidoVenta.objects.get(idPedidoVenta=id)
    cliente = Cliente.objects.get(idCliente=pedidoVenta.cliente_id)
    trabajador = Trabajador.objects.get(idTrabajador=pedidoVenta.trabajador_id)
    detalle = DetallePedidoVenta.objects.all().select_related('producto').filter(pedidoVenta=id).filter(eliminado=False)
    documento = DocumentoVenta.objects.get(pedidoVenta=id)


    data = {
        'cliente':cliente,
        'pedidoVenta': pedidoVenta,
        'documento':documento,
        'detalle': detalle,
        'trabajador':trabajador,
        'pdf_page_size': 'A6', 
    }
    pdf = render_to_pdf('pedidoVenta/listview.html', data, 'mi_ticket')

    #pdf = render_to_pdf('pedidoVenta/listview.html', data)
    return HttpResponse(pdf, content_type='application/pdf')



def generar_qr(request):
    # URL del PDF que deseas enlazar
    url_pdf = 'http://127.0.0.1:8000/pedidoVenta/pdf/4'

    # Genera el código QR en una imagen
    qr_img = qrcode.make(url_pdf)

    # Guarda la imagen en memoria
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)

    # Convierte la imagen a una cadena base64
    qr_img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    print(qr_img_base64)

    # Renderiza el contenido de la plantilla con el código QR
    context = {'qr_img_base64': qr_img_base64}
    qr_html = render_to_string('pedidoVenta/listview.html', context)

    # Devuelve la respuesta con el HTML que incluye el código QR
    return HttpResponse(qr_html)