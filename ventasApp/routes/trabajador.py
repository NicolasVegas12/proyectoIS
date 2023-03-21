
from django.urls import path
from ventasApp.views import trabajador

urlpatterns = [
    path('',trabajador.listartrabajador,name="listartrabajador"),
    path('create/',trabajador.agregartrabajador ,name="agregartrabajador"),
    path('edit/<int:id>/',trabajador.editartrabajador ,name="editartrabajador"),
    path('delete/<int:id>/',trabajador.eliminartrabajador,name="eliminartrabajador"), 
    path('active/<int:id>/<int:activo>/',trabajador.activartrabajador,name="activartrabajador"), 
]