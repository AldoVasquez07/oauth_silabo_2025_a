from django.db import models
from django.contrib.auth.models import AbstractUser

# ─────────────────────────────────────────────
#  SEGURIDAD Y USUARIOS
# ─────────────────────────────────────────────

class Rol(models.Model):
    nombre = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, related_name="usuarios")
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  # <-- ESTA LÍNEA ES CLAVE
    REQUIRED_FIELDS = ['username']  # Solo si aún quieres que username exista

    def __str__(self):
        return self.email



class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    apellido_paterno = models.CharField(max_length=200)
    apellido_materno = models.CharField(max_length=200)
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=[("M", "Masculino"), ("F", "Femenino")])
    nacionalidad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True)
    usuario = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name="persona")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno}, {self.nombre}"


class LogProcesos(models.Model):
    fecha = models.DateField()
    accion = models.TextField()
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="logs")

    def __str__(self):
        return f"{self.fecha} - {self.accion[:50]}"