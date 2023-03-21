from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import PedidoVenta 
from django.db.models import Q 
from ventasApp.forms import PedidoVenta
import datetime

def dashboard(request):
    return render(request, "dashboard/dashboard.html")


