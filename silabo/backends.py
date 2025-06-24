# tokens/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Autenticando {username}")
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            print(f"Usuario encontrado: {user}")
        except User.DoesNotExist:
            print("No existe el usuario")
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            print("Contraseña correcta y usuario autenticable")
            return user
        print("Fallo autenticación")
        return None
