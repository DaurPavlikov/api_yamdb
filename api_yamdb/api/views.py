from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from users.serializers import SignupSerializer, TokenSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TokenViewSet(viewsets.ViewSet):

    permission_classes = [permissions.AllowAny, ]

    def gettoken(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                'Неверный confirmation code',
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})


class SignupViewSet(viewsets.ViewSet):

    permission_classes = [permissions.AllowAny, ]

    def create(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(email=email, username=username).exists():
            user = get_object_or_404(User, email=email, username=username)
        else:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        return Response({'confirmation_code': confirmation_code})
