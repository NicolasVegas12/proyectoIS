
from django.urls import path
from seguridadApp.views.rol import *

urlpatterns = [
    path('',listarrole,name="listarrole"),     
    path('create/',agregarrole ,name="agregarrole"),
    path('edit/<int:id>/',editarrole ,name="editarrole"),
    path('delete/<int:id>/',eliminarrole,name="eliminarrole"), 
]