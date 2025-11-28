from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .serializers import (
    PasswordResetRequestSerializer,
    RegisterSerializer,
    SetNewPasswordSerializer
)


# Create your views here.


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({"message": "Correo enviado", "data": data})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Token inválido o expirado"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Contraseña cambiada correctamente"})
