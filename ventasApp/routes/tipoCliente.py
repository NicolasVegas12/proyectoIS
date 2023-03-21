
from django.urls import path
from ventasApp.views import tipoCliente

urlpatterns = [
    path('',tipoCliente.listartipoCliente,name="listartipoCliente"),
    path('create/',tipoCliente.agregartipoCliente ,name="agregartipoCliente"),
    path('edit/<int:id>/',tipoCliente.editartipoCliente ,name="editartipoCliente"),
    path('delete/<int:id>/',tipoCliente.eliminartipoCliente,name="eliminartipoCliente"), 
    path('active/<int:id>/<int:activo>/',tipoCliente.activartipoCliente,name="activartipoCliente"), 
]