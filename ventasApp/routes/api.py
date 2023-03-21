
from django.urls import path
from ventasApp.views.api import *

urlpatterns = [
    path('get_countCompras/',get_countCompras ,name="get_countCompras"),
    path('get_countVentas/',get_countVentas ,name="get_countVentas"),
    path('get_dataDona/',get_dataDona,name="get_dataDona"), 
    path('get_dataLine/',get_dataLine,name="get_dataLine"), 
    
    path('get_detallePedidoVenta/<int:id>/',obtenerDetallePedidoVenta,name="detallepedidoVenta"),
    path('get_detalleOrdenCompra/<int:id>/',obtenerDetalleOrdenCompra,name="detalleordenCompra"),
    path('get_detalleNotaAlmacen/<int:id>/',obtenerDetalleNotaAlmacen,name="detallenotaAlmacen"),
    path('get_tipoNotaAlmacen/<int:id>/',obtenerTipoNotaAlmacen,name="tipoNotaAlmacen"),
    
    path('get_cliente/<int:id>/',obtenerCliente,name="obtenerCliente"),
    path('get_proveedor/<int:id>/',obtenerProveedor,name="obtenerProveedor"),
]