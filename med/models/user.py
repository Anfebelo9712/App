from random import choices
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a user with the given username and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
def create_superuser(self, username, password):
    """
    Creates and saves a superuser with the given username and password.
    """
    user = self.create_user(
    username=username,
    password=password,
    )
    user.is_admin = True
    user.save(using=self._db)
    return user
class Usuario(AbstractBaseUser, PermissionsMixin):
    
    class AplicationRol(models.TextChoices):
        MED = 'MEDICO'
        ENF = 'ENFERMER@'
        PAC = 'PACIENTE'
        FAM = 'FAMILIAR'
        AUX ='AUXILIAR'


    id = models.BigAutoField(primary_key=True)
    username = models.CharField('username', max_length = 120, unique=True)
    password = models.CharField('password', max_length = 120)
    create_date = models.DateField('Create_date')
    activo = models.BooleanField(default=True)
    nombre = models.CharField('nombre',max_length=30)
    apellido = models.CharField('apellido',max_length=30)
    correo = models.EmailField('correo',max_length=100)
    direccion = models.CharField('direccion',max_length=30)
    telefono = models.CharField('telefono',max_length=30)
    
    rol = models.CharField(
        max_length=30,
        choices =AplicationRol.choices,
        default =AplicationRol.PAC,

    )
    
    def save(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)
    objects = UserManager()
    USERNAME_FIELD = 'username'