from rest_framework import serializers
from ventasApp.models import Cliente

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


