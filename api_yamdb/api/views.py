from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from users.models import User
from users.permissions import IsAutorModeratorAdminOrReadOnly, IsAdminOrReadOnly, IsAdmin
from api.filters import TitleFilter
from api.serializers import (CategoriesSerializer,
                             GenresSerializer,
                             TitlesSerializer, TitlesViewSerializer)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesViewSerializer
        return TitlesSerializer


class ReviewGenreModelMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAutorModeratorAdminOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoriesViewSet(ReviewGenreModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ReviewGenreModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
