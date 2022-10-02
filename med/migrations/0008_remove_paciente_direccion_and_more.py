# Generated by Django 4.1.1 on 2022-09-29 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0007_usuario_direccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='fecha_creacion',
        ),
        migrations.AlterField(
            model_name='auxiliar',
            name='cargo',
            field=models.CharField(max_length=80, verbose_name='cargo'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='id_registro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_registro_auxiliar', to='med.auxiliar'),
        ),
    ]
