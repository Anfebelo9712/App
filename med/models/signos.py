from django.db import models

from med.models.paciente import Paciente
from .historia import Historia
from .familiar import Familiar
from .paciente import Paciente


class Signos(models.Model):
    id_signos_vitales = models.BigAutoField(primary_key=True)
    oximetria = models.IntegerField('oximetria')
    frecuencia_respiratoria = models.CharField(null=True, max_length=20)
    frecuencia_cardiaca = models.CharField(null=True, max_length=20)
    temperatura = models.CharField(null=True, max_length=20)
    presion_arterial = models.CharField(null=True, max_length=20)
    glicemias = models.CharField(null=True, max_length=20)
    id_historias = models.ForeignKey(
        Historia, related_name='id_signos_historia', on_delete=models.CASCADE)
    id_familiar = models.ForeignKey(
        Familiar, related_name='id_familiar_signos', on_delete=models.CASCADE)
    id_paciente = models.ForeignKey(
        Paciente, related_name='id_paciente_signos', on_delete=models.CASCADE)
