# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        persona = getattr(user, 'persona', None)

        token['email'] = user.email
        token['rol']   = user.rol.nombre if user.rol else None
        token['nombre'] = (
            f"{persona.nombre} {persona.apellido_paterno} {persona.apellido_materno}"
            if persona else ""
        )

        return token

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')

        data = super().validate(attrs)

        persona = getattr(self.user, 'persona', None)
        data.update({
            'username': self.user.username,                     # si aún lo necesitas
            'email':    self.user.email,
            'rol':      self.user.rol.nombre if self.user.rol else None,
            'nombre': (
                f"{persona.nombre} {persona.apellido_paterno} {persona.apellido_materno}"
                if persona else ""
            ),
        })
        return data
