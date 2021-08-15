from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.validators import UniqueValidator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким username уже существует'
        )]
    )

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role',)
        model = User


class CustomTokenObtainSerializer(serializers.Serializer):
    '''
    Получить токен.

    Аргументы запроса:
    email - email пользователя, для которого требуется получить токен
    confirmation_code - код, полученный при регистрации
    '''
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        email = data['email']
        confirmation_code = data['confirmation_code']
        user = User.objects.filter(
            email=email,
            confirmation_code=confirmation_code,
            is_active=1
        ).first()
        if user is None:
            raise serializers.ValidationError(
                {'detail': 'Пользователь не существует или '
                           'confirmation code не верен'})
        token = {'token': str(AccessToken.for_user(user))}
        return token
