from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Indicamos que el campo para auth es email

    def validate(self, attrs):
        # Usamos correo y contraseña desde attrs
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise serializers.ValidationError('No se pudo autenticar con estas credenciales.')

        else:
            raise serializers.ValidationError('Debe incluir correo y contraseña.')

        attrs['user'] = user
        # Luego llama al método padre para generar tokens
        return super().validate({
            self.username_field: email,
            'password': password,
        })
