from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import TitleFilter
from .models import Category, Genre, Title
from users.permission import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadOnlySerializer, TitleWriteSerializer)


class CustomViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleWriteSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-id')
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadOnlySerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
