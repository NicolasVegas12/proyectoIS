
from django.urls import path
from ventasApp.views import producto

urlpatterns = [
    path('',producto.listarproducto,name="listarproducto"),
    path('create/',producto.agregarproducto ,name="agregarproducto"),
    path('edit/<int:id>/',producto.editarproducto ,name="editarproducto"),
    path('delete/<int:id>/',producto.eliminarproducto,name="eliminarproducto"), 
    path('active/<int:id>/<int:activo>/',producto.activarproducto,name="activarproducto"), 
]