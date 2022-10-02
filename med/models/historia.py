from django.db import models
from .paciente import Paciente
from .medico import Medico
from .enfermero import Enfermero
from .familiar import Familiar


class Historia (models.Model):
	id_historia_c = models.AutoField(primary_key=True)
	id_paciente = models.ForeignKey(
	    Paciente, related_name='id_historia_paciente', on_delete=models.CASCADE)
	id_medico = models.ForeignKey(
	    Medico, related_name='id_historia_medico', on_delete=models.CASCADE)
id_enfermero = models.ForeignKey(Enfermero, related_name='id_historia_enfermero', on_delete= models.CASCADE)
id_familiar = models.ForeignKey(Familiar,related_name='id_historia_familiar', on_delete= models.CASCADE)
diagnostico= models.TextField(null=True, max_length=2000)
entorno= models.CharField(null=True, max_length=20)
sugerencias = models.TextField(null=True, max_length=2000)