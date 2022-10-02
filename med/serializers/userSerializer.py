from rest_framework import serializers
from med.models import Usuario


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Usuario
        fields = ['username','password','activo','nombre','apellido','create_date','correo','direccion','telefono','rol']

        def create(self,validated_data):
            userInstance = Usuario.objects.create( **validated_data)
            return userInstance
