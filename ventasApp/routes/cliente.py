
from django.urls import path
from ventasApp.views import cliente

urlpatterns = [
    path('',cliente.listarcliente,name="listarcliente"),
    path('create/',cliente.agregarcliente ,name="agregarcliente"),
    path('edit/<int:id>/',cliente.editarcliente ,name="editarcliente"),
    path('delete/<int:id>/',cliente.eliminarcliente,name="eliminarcliente"), 
    path('active/<int:id>/<int:activo>/',cliente.activarcliente,name="activarcliente"), 
]