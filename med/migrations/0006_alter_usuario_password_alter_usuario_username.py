# Generated by Django 4.1.1 on 2022-09-27 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0005_alter_usuario_password_alter_usuario_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=120, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=120, unique=True, verbose_name='username'),
        ),
    ]
