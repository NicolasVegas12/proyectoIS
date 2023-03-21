
from django.urls import path
from ventasApp.views import formaPago

urlpatterns = [
    path('',formaPago.listarformaPago,name="listarformaPago"),
    path('create/',formaPago.agregarformaPago ,name="agregarformaPago"),
    path('edit/<int:id>/',formaPago.editarformaPago ,name="editarformaPago"),
    path('delete/<int:id>/',formaPago.eliminarformaPago,name="eliminarformaPago"), 
    path('active/<int:id>/<int:activo>/',formaPago.activarformaPago,name="activarformaPago"), 
]