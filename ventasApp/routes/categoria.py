
from django.urls import path
from ventasApp.views import categoria

urlpatterns = [
    path('',categoria.listarcategoria,name="listarcategoria"),
    path('create/',categoria.agregarcategoria ,name="agregarcategoria"),
    path('edit/<int:id>/',categoria.editarcategoria ,name="editarcategoria"),
    path('delete/<int:id>/',categoria.eliminarcategoria,name="eliminarcategoria"), 
    path('active/<int:id>/<int:activo>/',categoria.activarcategoria,name="activarcategoria"), 
]