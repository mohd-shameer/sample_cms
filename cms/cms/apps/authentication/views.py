from django.contrib.auth import authenticate, login

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from cms.apps.authentication import models
from .serializers import CustomUserSerializer


class UserViewset(viewsets.ModelViewSet):
    model = models.CustomUser
    queryset = models.CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = self.model.objects.all()
            return queryset.filter(email=self.request.user.email)
        return super().get_queryset()


class Login(APIView):

    def post(self, request, *args, **kwargs):
        creds = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        user = authenticate(**creds)
        if not user:
            raise exceptions.AuthenticationFailed("Invalid credentials")

        login(request, user)
        auth_obj, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Login successfull.",
                         "token": str(auth_obj.key)})
