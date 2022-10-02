from django.db import models
from .user import Usuario
    
class Auxiliar(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario,related_name = 'id_usuario_aux',on_delete=models.CASCADE,unique=True)
    cargo = models.CharField('cargo',max_length=80)
    
    