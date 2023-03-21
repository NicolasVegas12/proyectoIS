
from django.urls import path
from ventasApp.views.ordenCompra import *

urlpatterns = [
    path('',listarordenCompra,name="listarordenCompra"),
    path('create/',agregarordenCompra ,name="agregarordenCompra"),
    path('edit/<int:id>/',editarordenCompra ,name="editarordenCompra"),
    path('delete/<int:id>/',eliminarordenCompra,name="eliminarordenCompra"), 
    path('active/<int:id>/<int:activo>/',activarordenCompra,name="activarordenCompra"),
     path('pdf/<int:id>',ListOrdenCompraPdf,name='pdfOrdenCompra'),
]