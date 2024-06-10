from ventasApp.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .userSerializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

