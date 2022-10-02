from datetime import datetime
from med.models import Usuario, Paciente, Auxiliar
from rest_framework import status, views
from med.serializers import UserSerializer, PacienteSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings


def validatePaciente(token,id_paciente):
   try:
    #token = request.META.get('HTTP_ATHORIZATION')[7:]
    tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])    
    valid_data = tokenBackend.decode(token, verify=False)
    paciente = Paciente.objects.get(id = id_paciente)
    usuario = Usuario.objects.get(id=paciente.usuario.id)
    paciente_novalido = paciente.usuario.id != valid_data['user_id'] or usuario.rol != Usuario.AplicationRol.PAC
    return paciente_novalido
   except:
    return True 


def validateAux(token, id_aux):
    try:
        #token = request.META.get('HTTP_ATHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)
        aux_registra = Auxiliar.objects.get(id=id_aux)
        usuario_auxiliar = Usuario.objects.get(id=aux_registra.usuario.id)
        tokenNoValido = aux_registra == valid_data['user_id'] != aux_registra.usuario.id or usuario_auxiliar.rol != Usuario.AplicationRol.AUX
        return tokenNoValido
    except:
        return True




class PacienteView(views.APIView):

 def post(self, request, *args, **kwargs):
        #VALIDACION DEL POST 
        try:
            token = request.META.get('HTTP_ATHORIZATION')[7:]
            tokenNoValido = validateAux(token,request.data['paciente_info']['id_registro'])
        except:
            stringResponse = {'detail':'No hay token'}
            return Response(stringResponse,status=status.HTTP_401_UNAUTHORIZED) 

        if tokenNoValido:
            stringResponse = {'detail':'UNAUTHORIZED REQUEST'}
            return Response(stringResponse,status=status.HTTP_401_UNAUTHORIZED) 
        # guardar el usuario
        data_usuario = request.data.pop('usuario_info')
        now = datetime.now()
        data_usuario['create_date'] = now.strftime("%Y-%m-%d")
        data_usuario['rol'] = Usuario.AplicationRol.PAC
        serializer_user = UserSerializer(data=data_usuario)
        serializer_user.is_valid(raise_exception=True)
        usuario = serializer_user.save()

        data_paciente = request.data.pop('paciente_info')
        data_paciente['id_usuario'] = usuario.id
        data_paciente['create_date'] = now.strftime("%Y-%m-%d")
        serializer_paciente = PacienteSerializer(data=data_paciente)
        serializer_paciente.is_valid(raise_exception=True)
        serializer_paciente.save()
        paciente = serializer_paciente.save()

        tokenData = {"username": data_usuario['username'], "password": data_usuario['password']}
        tokenSerializer = TokenObtainPairSerializer(data=tokenData)
        tokenSerializer.is_valid(raise_exception=True)
        return_data = {'paciente': PacienteSerializer(paciente).data,
                        "token_data": tokenSerializer.validated_data}
        return Response(return_data, status=status.HTTP_201_CREATED)



def delete(self, request, *args, **kwargs):
    
        try:
            token = request.META.get('HTTP_ATHORIZATION')[7:]
            ValidacionPaciente = validatePaciente(request, **kwargs['pk'])
            if ValidacionPaciente:
                validacionAuxiliar= validateAux (token,kwargs['id_elimina']) #validar los tipos de usuarios que pueden eliminar
            else:
               validacionAuxiliar = False
        
        
        except:
            stringResponse = {'detail':'No hay token'}
            return Response(stringResponse,status=status.HTTP_401_UNAUTHORIZED) 

        if validacionAuxiliar and  ValidacionPaciente: #Si no es valido el susario arroja el return
            stringResponse = {'detail':'UNAUTHORIZED REQUEST'}
            return Response(stringResponse,status=status.HTTP_401_UNAUTHORIZED) 
        
        paciente = Paciente.objects.filter(id = kwargs['pk']).first()
        usuario = Usuario.objects.filter(id=paciente.usuario.id).first()

        paciente.delete()
        usuario.delete()

        stringResponse = {'detail': ' Registro eliminado exitosamente'}
        return Response(stringResponse, status = status.HTTP_200_OK)


    # Buscar todos los pacientes.
def get(self,request, *args, **kwargs):

        pacienteNovalido = True
        auxiliarNovalido = True
        try:
            token=request.META.get( 'HTTP_AUTHORIZATION')[7:] 
            pacienteNovalido = validatePaciente(token,kwargs['pk'])
            auxiliarNovalido = validateAux(token,kwargs['id_elimina']) 
        except:
            stringResponse= {'detail':'no hay token valido'}
            return stringResponse
       
        if auxiliarNovalido and pacienteNovalido:
            stringResponse = {'detail':'Unauthorized request'}
            return Response(stringResponse,status=status.HTTP_401_UNAUTHORIZED)
         
        
        paciente = Paciente.objects.all()
        paciente_serializer = PacienteSerializer(paciente,many=True)
        return Response(paciente_serializer.data)

def put(self, request, *args, **kwargs):
        paciente = Paciente.objects.get(id=kwargs['pk']) ##busca por Pk
        usuario =  Usuario.objects.get(id=paciente.id_usuario.id)
        now = datetime.now() ##fecha de actualziacion

        data_usuario = request.data.pop('usuario_info')
        data_usuario['create_date'] = now.strftime("%Y-%m-%d")

        serializer_user = UserSerializer(usuario,data = data_usuario)
        serializer_user.is_valid(raise_exception=True)
        usuario = serializer_user.save()

        data_paciente = request.data.pop('paciente_info')
        data_paciente['create_date'] = now.strftime("%Y-%m-%d")
        data_paciente['usuario'] = usuario.id

        serializer_paciente = PacienteSerializer(paciente,data=data_paciente)
        serializer_paciente.is_valid(raise_exception=True)
        serializer_paciente.save()
        paciente = serializer_paciente.save()

        return_data = {'paciente':PacienteSerializer(paciente).data}
        return Response(return_data, status = status.HTTP_200_OK)

def AllPacientes(self,request, *args, **kwargs):
        
        paciente = Paciente.objects.all()
        paciente_serializer = PacienteSerializer(paciente,many=True)
        return Response(paciente_serializer.data)