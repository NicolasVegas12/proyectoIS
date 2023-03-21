from django.shortcuts import render,redirect 
from django.http import JsonResponse
from ventasApp.models import * 

def get_countVentas(request,*args,**kwargs):
    cantidad = PedidoVenta.objects.filter(eliminado=False).count()
    data={
        'tipo':'ventas',
        'cantidad': cantidad
    }
    return JsonResponse(data)

def get_countCompras(request,*args,**kwargs):
    cantidad = OrdenCompra.objects.filter(eliminado=False).count()
    data={
        'tipo':'compras',
        'cantidad':cantidad
    }
    return JsonResponse(data)

def get_dataLine(request,*args,**kwargs):
    list_trabajadores = []
    list_ventasxtrabajador = []
    trabajadores = Trabajador.objects.all().filter(eliminado=False).order_by('-idTrabajador').values()
    for t in trabajadores:
        trabajador = Trabajador.objects.get(idTrabajador=t['idTrabajador'])
        cuenta = PedidoVenta.objects.filter(trabajador=trabajador).filter(eliminado=False).count()
        list_trabajadores.append(str(t['apellidos'])+str(' ')+str(t['nombres']))
        list_ventasxtrabajador.append(cuenta)
    data = {
          'labels': list_trabajadores,
          'datasets': [{
            'label': 'Cantidad de Ventas',
            'backgroundColor': 'rgb(255, 99, 132)',
            'borderColor': 'rgb(255, 99, 132)',
            'data': list_ventasxtrabajador,
          }]
    };
    return JsonResponse(data)

def get_dataDona(request,*args,**kwargs):
    list_productos = []
    list_cantidadvendidos = []
    productos = Producto.objects.all().filter(eliminado=False).order_by('-idProducto').values()
    for t in productos:
        producto = Producto.objects.get(idProducto=t['idProducto'])
        cuenta = DetallePedidoVenta.objects.filter(producto=producto).filter(eliminado=False).count()
        list_productos.append(str(t['nombre']))
        list_cantidadvendidos.append(cuenta)
    data = {
            'labels': list_productos,
            'datasets': [{
                'label': '# of Votes',
                'data': list_cantidadvendidos,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                'borderWidth': 1
            }]
        };
    return JsonResponse(data)



def obtenerDetallePedidoVenta(request,*args,**kwargs):
    list_detalle = []
    pedidoVenta=PedidoVenta.objects.get(idPedidoVenta=kwargs['id'])
    listado = DetallePedidoVenta.objects.all().filter(pedidoVenta=pedidoVenta).filter(eliminado=False).values()
    for t in listado:  
        producto=Producto.objects.get(idProducto=t['producto_id'])      
        list_detalle.append({
            'detalle_id': t['idDetallePedidoVenta'],
            'producto_id':producto.idProducto,
            'stock':producto.stock,
            'codigo':producto.codigo,
            'descripcion':producto.descripcion,
            'cantidad':t['cantidad'],
            'precioUnitario':t['precioUnitario'],
            'descuentoUnitario':t['descuentoUnitario'],
            'precio':t['precio'],
        })
    cliente = Cliente.objects.get(idCliente=pedidoVenta.cliente_id)
    documento = DocumentoVenta.objects.get(pedidoVenta=pedidoVenta)
    data={
        'idPedidoVenta':pedidoVenta.idPedidoVenta,
        'tasaIgv':pedidoVenta.tasaIgv,
        'serie' : documento.serie,
        'numero' : documento.numero,
        'subtotal':pedidoVenta.subtotal,
        'descuento':pedidoVenta.descuento,
        'total':pedidoVenta.total,
        'detalle':list_detalle
    }
    
    return JsonResponse(data)


def obtenerDetalleOrdenCompra(request,*args,**kwargs):
    list_detalle = []
    ordenCompra=OrdenCompra.objects.get(idOrdenCompra=kwargs['id'])
    listado = DetalleOrdenCompra.objects.all().filter(ordenCompra=ordenCompra).filter(eliminado=False).values()
    for t in listado:  
        producto=Producto.objects.get(idProducto=t['producto_id'])      
        list_detalle.append({
            'detalle_id': t['idDetalleOrdenCompra'],
            'producto_id':producto.idProducto,
            'stock':producto.stock,
            'codigo':producto.codigo,
            'descripcion':producto.descripcion,
            'cantidad':t['cantidad'],
            'precioUnitario':t['precioUnitario'],
            'descuentoUnitario':t['descuentoUnitario'],
            'precio':t['precio'],
        })
    proveedor = Proveedor.objects.get(idProveedor=ordenCompra.proveedor_id)
    documento = DocumentoCompra.objects.get(ordenCompra=ordenCompra)
    data={
        'idPedidoVenta':ordenCompra.idOrdenCompra,
        'tasaIgv':ordenCompra.tasaIgv,
        'serie':documento.serie,
        'numero':documento.numero,
        'subtotal':ordenCompra.subtotal,
        'descuento':ordenCompra.descuento,
        'total':ordenCompra.total,
        'detalle':list_detalle
    }
    
    return JsonResponse(data)

def obtenerTipoNotaAlmacen(request,*args,**kwargs):
    notaAlmacen=NotaAlmacen.objects.get(idNotaAlmacen=kwargs['id'])
    if notaAlmacen.ordenCompra_id != None:
        tipo = 1
    else :
        tipo = 2

    data={
        'tipo': tipo
    }
    return JsonResponse(data)    

def obtenerDetalleNotaAlmacen(request,*args,**kwargs):
    
    list_detalle = []
    notaAlmacen=NotaAlmacen.objects.get(idNotaAlmacen=kwargs['id'])
    listado = DetalleNotaAlmacen.objects.all().filter(notaAlmacen=notaAlmacen).filter(eliminado=False).values()
    for t in listado:  
        producto=Producto.objects.get(idProducto=t['producto_id'])      
        list_detalle.append({
            'detalle_id': t['idDetalleNotaAlmacen'],
            'producto_id':producto.idProducto,
            'stock':producto.stock,
            'codigo':producto.codigo,
            'descripcion':producto.descripcion,
            'cantidad':t['cantidad'],
            'precioUnitario':t['precioUnitario'],
            'descuentoUnitario':t['descuentoUnitario'],
            'precio':t['precio'],
        })
    data={
        'idPedidoVenta':notaAlmacen.idNotaAlmacen,
        'subtotal':notaAlmacen.subtotal,
        'descuento':notaAlmacen.descuento,
        'total':notaAlmacen.total,
        'detalle':list_detalle
    }
    
    return JsonResponse(data)


def obtenerCliente(request,*args,**kwargs):
    cliente = Cliente.objects.get(idCliente=kwargs['id'])

    data={
        'idCliente':cliente.idCliente,
        'tipoDocumentoIdentidad':cliente.tipoDocumentoIdentidad,
        'documentoIdentidad':cliente.documentoIdentidad,
    }
    
    return JsonResponse(data)

def obtenerProveedor(request,*args,**kwargs):
    proveedor = Proveedor.objects.get(idProveedor=kwargs['id'])

    data={
        'idProveedor':proveedor.idCliente,
        'ruc':proveedor.ruc,
        'razonSocial':proveedor.razonSocial,
    }
    
    return JsonResponse(data)