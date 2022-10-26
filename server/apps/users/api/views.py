from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters, generics, permissions, status

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token

from apps.users.api.serializers import RegisterSerializer, EmailVerificationSerializer, MyTokenObtainPairSerializer, \
    UpdatePasswordSerializer
from apps.users.models import User
from apps.users.tasks import activate_user
from rest_framework.decorators import api_view, permission_classes

from storage.ftp import FTPStorage


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        # our access token
        token = RefreshToken.for_user(user).access_token
        # our current domain
        current_site = get_current_site(request).domain
        # email verify link
        relative_link = reverse('email-verify')
        # absolute path
        abs_url = f'http://{current_site}{relative_link}?token={token}'
        # email body
        email_body = f'Hi {user.username}, use link below to verify\n{abs_url}'
        data = {'email_body': email_body, 'email_subject': 'Verify your email', 'receivers': user.email}
        activate_user.delay(data)
        return Response(user_data, status.HTTP_201_CREATED)


class VerifyEmailAPIView(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'success activate'}, status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as ex:
            return Response({'error': 'activation is expired'}, status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as ex:
            return Response({'error': 'invalid token'}, status.HTTP_400_BAD_REQUEST)


class UpdatePasswordAPIView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        # return new token
        return Response('success', status=status.HTTP_200_OK)


class ResetPasswordRequestAPIView(views.APIView):
    def get(self, request):
        pass


class SetNewPasswordAPIView(views.APIView):
    def post(self):
        pass


class LogoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response('successful logout', status=status.HTTP_205_RESET_CONTENT)
        except Exception as ex:
            return Response(f'{ex}', status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request: Request):
    pass
