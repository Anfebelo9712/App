from django.db import models
from .user import Usuario
from .auxiliar import Auxiliar

class Familiar(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario,related_name = 'id_usuario_familiar',on_delete=models.CASCADE,unique=True)
    create_date = models.DateField('create_date')
    relacion = models.CharField('Paretesco con paciente',max_length=20,null=True)
    id_registra = models.ForeignKey(Auxiliar,related_name = 'id_auxiliar_registro_familiar',on_delete=models.CASCADE)
