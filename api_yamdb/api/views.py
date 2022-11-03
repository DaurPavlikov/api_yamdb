from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import (
    serializers, viewsets, filters, mixins, status, permissions)
from rest_framework.response import Response
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination)
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review, Title, Category, Genre
from users.permissions import (
    IsAutorModeratorAdminOrReadOnly, IsAdminOrReadOnly, IsAdmin)
from users.serializers import SignupSerializer, TokenSerializer
from users.models import User
from api.filters import TitleFilter
from api.serializers import (CategoriesSerializer,
                             GenresSerializer,
                             TitlesSerializer,
                             TitlesViewSerializer,
                             CommentSerializer,
                             ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAutorModeratorAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title,
                                 author=self.request.user).exists():
            raise serializers.ValidationError('Вы уже оставили коммент')
        serializers.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAutorModeratorAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()


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
    queryset = Title.objects.annotate(rating=Avg('review__score'))
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