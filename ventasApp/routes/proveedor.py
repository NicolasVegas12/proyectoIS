
from django.urls import path
from ventasApp.views import proveedor

urlpatterns = [
    path('',proveedor.listarproveedor,name="listarproveedor"),
    path('create/',proveedor.agregarproveedor ,name="agregarproveedor"),
    path('edit/<int:id>/',proveedor.editarproveedor ,name="editarproveedor"),
    path('delete/<int:id>/',proveedor.eliminarproveedor,name="eliminarproveedor"), 
    path('active/<int:id>/<int:activo>/',proveedor.activarproveedor,name="activarproveedor"), 
]