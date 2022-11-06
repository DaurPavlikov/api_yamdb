from rest_framework import serializers
from django.core.validators import MinLengthValidator
from rest_framework.validators import UniqueValidator

from .models import User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[
        MinLengthValidator(
            3,
            message='username must be longer than 2 characters'
        ),
        UniqueValidator(queryset=User.objects.all())
    ])
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all())
    ])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class SignupSerializer(UserSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User
