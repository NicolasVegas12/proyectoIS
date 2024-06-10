from ventasApp.models import Cliente
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .clientSerializer import ClientSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientSerializer



@api_view(['POST'])
def login_api_view(request):
    user = Cliente.objects.filter()
