from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title
from users.models import User
from users.permissions import IsAutorModeratorAdminOrReadOnly, IsAdminOrReadOnly, IsAdmin
from users.serializers import SignupSerializer, TokenSerializer
from api.filters import TitleFilter
from api.serializers import (CategoriesSerializer,
                             GenresSerializer,
                             TitlesSerializer, TitlesViewSerializer)

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
