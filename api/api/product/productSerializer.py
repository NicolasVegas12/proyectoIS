from rest_framework import serializers
from ventasApp.models import Producto

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
