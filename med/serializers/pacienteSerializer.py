from med.models.user import Usuario
from med.models import Paciente
from med.models import Usuario
from rest_framework import serializers
from datetime import datetime

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id','id_usuario','ciudad','id_registro']

    def create(self,validate_data):
        pacienteInstance = Paciente.objects.create(**validate_data)
        return pacienteInstance

    def to_representation(self,obj):
        paciente = Paciente.objects.get(id=obj.id)
        user = Usuario.objects.get(id=paciente.id_usuario.id)

        return{
            'paciente':{
                'id_paciente' : paciente.id,
                'id_registro' : paciente.id_registro,
            },
            'usuario': {
                'id_usuario': user.id,
                'username' : user.username,
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

