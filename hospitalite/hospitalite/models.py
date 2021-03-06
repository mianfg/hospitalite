from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField

PROVINCIAS = ("Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León", "Lérida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza")

class Usuario (AbstractUser):
    # Código de usuario generado
    username = models.CharField(max_length = 6, primary_key=True)
    dni = models.CharField(max_length=9)
    first_name = models.CharField(max_length = 20, verbose_name="nombre")
    last_name = models.CharField(max_length = 60, verbose_name="apellidos")
    provincia = models.CharField(max_length = 10)
    localidad = models.CharField(max_length = 20)
    skype = models.CharField(max_length = 15)
    facetime = models.CharField(max_length = 20)
    edad = models.IntegerField(default=-1) # TODO CAMBIAR A FECHA NAC

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    def is_voluntario(self):
        return len(Voluntario.objects.filter(username=self.username))!=0
    
    def get_group(self):
        if self.is_voluntario():
            return 'voluntario'
        else:
            return 'no_voluntario'
    
    def serialize(self):
        data = {
            'username'      : self.username,
            'dni'           : self.dni,
            'first_name'    : self.first_name,
            'last_name'     : self.last_name,
            'provincia'     : self.provincia,
            'localidad'     : self.localidad,
            'skype'         : self.skype,
            'facetime'      : self.facetime,
            'edad'          : self.edad
        }
        
        return data
        
class Voluntario(models.Model):
    username = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key = True)
    email = models.EmailField()
    telefono = PhoneField()
    ocupacion = models.CharField(max_length = 20)
    consentimiento = models.BooleanField()
    verificado = models.BooleanField(default=False)

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    username1 = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='usuario1')
    username2 = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='usuario2')

class Rating(models.Model):
    id_match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    from_user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    comentario = models.CharField(max_length=140)

    class Meta:
        unique_together = (("id_match", "from_user"),)

class MatchingQueue(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    username = models.ForeignKey(Usuario, on_delete=models.CASCADE)