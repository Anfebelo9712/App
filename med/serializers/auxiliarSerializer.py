from med.models.user import Usuario
from med.models import Auxiliar
from med.models import Usuario
from rest_framework import serializers
from datetime import datetime

class AuxiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auxiliar
        fields = ['id','id_usuario','cargo']

    def create(self,validate_data):
        auxiliarInstance = Auxiliar.objects.create(**validate_data)
        return auxiliarInstance

    def to_representation(self,obj):
        auxiliar = Auxiliar.objects.get(id=obj.id)
        user = Usuario.objects.get(id=auxiliar.id_usuario.id)

        return{
            'auxiliar':{
                'id_auxiliar' : auxiliar.id,
                'cargo': auxiliar.cargo,
            },
            'usuario': {
                'id_usuario': user.id,
                'Username' : user.username,
                'Password' : user.password,
                'nombre': user.nombre,
                'apellido': user.apellido,
                'create_date' : user.create_date,
                'activo': user.activo,
                'correo': user.correo,
                'direccion' : user.direccion,
                'telefono': user.telefono,
                'rol':user.rol,
             }
        }

