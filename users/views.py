from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api_yamdb.settings import EMAIL_FROM, EMAIL_SUBJ, EMAIL_TEXT

from .permission import IsAdmin
from .serializer import CustomTokenObtainSerializer, UserSerializer

User = get_user_model()


class CreateUser(generics.CreateAPIView):
    '''
    Создать пользователя, получить код подтверждения на email.

    Аргументы запроса:
    email - email пользователя
    '''
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        confirmation_code = get_random_string(length=12)
        if username is None:
            username = email.split('@')[0]
        User.objects.update_or_create(
            email=email,
            username=username,
            defaults={'confirmation_code': confirmation_code}
        )
        send_mail(
            EMAIL_SUBJ,
            EMAIL_TEXT.format(confirmation_code=confirmation_code),
            EMAIL_FROM,
            [email],
            fail_silently=False
        )
        return Response(
            'На указанную почту отправлено письмо с confirmation_code',
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    '''
    Получить список пользователей.

    Поле для поиска - username.
    Поле для фильтрации - username.
    '''
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(User, username=request.user)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
