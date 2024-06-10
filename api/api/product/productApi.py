from ventasApp.models import Producto
from rest_framework import viewsets, permissions
from .productSerializer import productSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = productSerializer