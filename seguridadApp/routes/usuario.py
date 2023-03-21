
from django.urls import path
from seguridadApp.views.usuarios import *

urlpatterns = [
    path('',listarusuario,name="listarusuario"),      
    path('create/',agregarusuario ,name="agregarusuario"),
    path('edit/<int:id>/',editarusuario ,name="editarusuario"),
    path('delete/<int:id>/',eliminarusuario,name="eliminarusuario"), 
    path('resetpassword/<int:id>/',resetpasswordusuario,name="resetpasswordusuario"), 
    path('active/<int:id>/<int:activo>/',activarusuario,name="activarusuario"), 
]