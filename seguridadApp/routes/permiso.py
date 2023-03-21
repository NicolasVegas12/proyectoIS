
from django.urls import path
from seguridadApp.views.permiso import *

urlpatterns = [
    path('',listarpermiso,name="listarpermiso"),  
]