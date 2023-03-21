
from django.urls import path
from ventasApp.views.pedidoVenta import *

urlpatterns = [
    path('',listarpedidoVenta,name="listarpedidoVenta"),
    path('create/',agregarpedidoVenta,name="agregarpedidoVenta"),
    path('edit/<int:id>/',editarpedidoVenta,name="editarpedidoVenta"),
    path('delete/<int:id>/',eliminarpedidoVenta,name="eliminarpedidoVenta"), 
    path('pdf/<int:id>',ListPedidoVentaPdf,name='pdfpedidoVenta'),
]