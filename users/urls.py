from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateUser, MyTokenObtainPairView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='UserView')
patterns_auth = [
    path('email/', CreateUser.as_view(), name='user_creat'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('v1/auth/', include(patterns_auth)),
    path('v1/', include(router.urls)),
]
