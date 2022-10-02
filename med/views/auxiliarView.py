from datetime import datetime
from hashlib import algorithms_available
from med.models import Usuario,Auxiliar
from rest_framework import status, views
from med.serializers import UserSerializer, AuxiliarSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated
from django.conf import settings 


class AuxiliarView(views.APIView):

    def post(self, request, *args, **kwargs):
        ##guardar el usuario
        data_usuario = request.data.pop('usuario_info')
        now = datetime.now()
        data_usuario['create_date'] = now.strftime("%Y-%m-%d")
        data_usuario['rol'] = Usuario.AplicationRol.AUX
        serializer_user = UserSerializer(data = data_usuario)
        serializer_user.is_valid(raise_exception=True)
        usuario = serializer_user.save()

        data_auxiliar = request.data.pop('auxiliar_info')
        data_auxiliar['id_usuario'] = usuario.id
        data_auxiliar['create_date'] = now.strftime("%Y-%m-%d")
        serializer_auxiliar = AuxiliarSerializer(data=data_auxiliar)
        serializer_auxiliar.is_valid(raise_exception=True)
        serializer_auxiliar.save()
        auxiliar = serializer_auxiliar.save()

        tokenData =  {"username":data_usuario['username'], "password":data_usuario['password']}
        tokenSerializer = TokenObtainPairSerializer(data=tokenData)
        tokenSerializer.is_valid(raise_exception=True)
        return_data = {'auxiliar': AuxiliarSerializer(auxiliar).data,
                        "token_data":tokenSerializer.validated_data}
        return Response(return_data, status = status.HTTP_201_CREATED) 

    

    def delete(self, request, *args, **kwargs):
        auxiliar = Auxiliar.objects.filter(id = kwargs['pk']).first()
        usuario = Usuario.objects.filter(id=auxiliar.id_usuario.id).first()

        auxiliar.delete()
        usuario.delete()

        stringResponse = {'detail': ' Registro eliminado exitosamente'}
        return Response(stringResponse, status = status.HTTP_200_OK)

    ##buscar por ID auxiliar
    def  get(self, request, *args, **kwargs):
        try: 
            token = request.META.get('HTTP_AUTHORIZATION')[7:]
            tokenBackend = TokenBackend(algorithm=settings.SIMPLEJWT['ALGORITHM'])
            valid_data = tokenBackend.decode(token,verify=False)
            auxiliar = Auxiliar.objects.get(id=kwargs['pk'])
            if valid_data['user_id'] != auxiliar.usuario.id:
                stringResponse = {'detail':'Unauthorized Request'}
                return Response(stringResponse, status= status.HTTP_401_UNAUTHORIZED)
        except:
            stringResponse = {'detail':'No hay token'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        auxiliar = Auxiliar.objects.get(id=kwargs['pk'])
        serializer_aux = AuxiliarSerializer(auxiliar)

        return Response(serializer_aux.data, status= status.HTTP_20O_OK)
    
    ##Buscar todos los Auxiliares.
    def AllAuxiliares(self,request, *args, **kwargs):
        auxiliar = Auxiliar.objects.all()
        auxiliar_serializer = AuxiliarSerializer(auxiliar,many=True)
        return Response(auxiliar_serializer.data)

    def put(self, request, *args, **kwargs):
        auxiliar = Auxiliar.objects.get(id=kwargs['pk']) ##busca por Pk
        usuario =  Usuario.objects.get(id=auxiliar.id_usuario.id)
        now = datetime.now() ##fecha de actualziacion

        data_usuario = request.data.pop('usuario_info')
        data_usuario['create_date'] = now.strftime("%Y-%m-%d")

        serializer_user = UserSerializer(usuario,data = data_usuario)
        serializer_user.is_valid(raise_exception=True)
        usuario = serializer_user.save()

        data_auxiliar = request.data.pop('auxiliar_info')
        data_auxiliar['create_date'] = now.strftime("%Y-%m-%d")
         

        serializer_auxiliar = AuxiliarSerializer(auxiliar,data=data_auxiliar)
        serializer_auxiliar.is_valid(raise_exception=True)
        serializer_auxiliar.save()
        auxiliar = serializer_auxiliar.save()

        return_data = {'auxiliar':AuxiliarSerializer(auxiliar).data}
        return Response(return_data, status = status.HTTP_200_OK)