# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes añadir info extra si deseas
        token['email'] = user.email
        token['rol'] = user.rol.nombre if user.rol else None
        return token

    def validate(self, attrs):
        # Redireccionar el valor de email a username (SimpleJWT usa 'username' internamente)
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
