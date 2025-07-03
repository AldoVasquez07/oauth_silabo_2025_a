# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ───── Extra claims dentro del JWT (opcional) ─────
        token['email'] = user.email
        token['rol']   = user.rol.nombre if user.rol else None

        # Datos personales
        if hasattr(user, 'persona') and user.persona:
            token['nombre']            = user.persona.nombre
            token['apellido_paterno']  = user.persona.apellido_paterno
            token['apellido_materno']  = user.persona.apellido_materno

        return token

    def validate(self, attrs):
        # SimpleJWT sigue buscando 'username'; mapea tu email ahí
        attrs['username'] = attrs.get('email')

        # Obtiene {'refresh': '...', 'access': '...'} y setea self.user
        data = super().validate(attrs)

        # ───── Campos adicionales que viajarán en la RESPUESTA ─────
        persona = getattr(self.user, 'persona', None)
        data.update({
            'username':          self.user.username,              # si aún lo usas
            'email':             self.user.email,
            'rol':               self.user.rol.nombre if self.user.rol else None,
            'nombre':            persona.nombre if persona else None,
            'apellido_paterno':  persona.apellido_paterno if persona else None,
            'apellido_materno':  persona.apellido_materno if persona else None,
        })
        return data
