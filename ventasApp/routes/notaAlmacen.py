
from django.urls import path
from ventasApp.views import notaAlmacen

urlpatterns = [
    path('',notaAlmacen.listarnotaAlmacen,name="listarnotaAlmacen"),
    path('create/',notaAlmacen.agregarnotaAlmacen ,name="agregarnotaAlmacen"),
    path('edit/<int:id>/',notaAlmacen.editarnotaAlmacen ,name="editarnotaAlmacen"),
    path('delete/<int:id>/',notaAlmacen.eliminarnotaAlmacen,name="eliminarnotaAlmacen"), 
    path('active/<int:id>/<int:activo>/',notaAlmacen.activarnotaAlmacen,name="activarnotaAlmacen"),
]