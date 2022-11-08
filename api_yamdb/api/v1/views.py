from django.db.models import Avg
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from reviews.models import Review, Title, Category, Genre
from users.permissions import (
    IsAutorModeratorAdminOrReadOnly,
    IsAdminOrReadOnly,
    IsAdmin,
)
from users.serializers import (
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
)
from users.models import User
from .filters import TitleFilter
from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesCreateSerializer,
    TitlesReadSerializer,
    CommentSerializer,
    ReviewsSerializer,
)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAutorModeratorAdminOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.select_related('author', 'review').all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAutorModeratorAdminOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.select_related('author', 'title').all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        detail=False, methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """Личные данные пользователя."""
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny, ]

    def signup(self, request):
        """Функция отправки кода подтверждения."""
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(email=email, username=username).exists():
            user = get_object_or_404(User, email=email, username=username)
        else:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        email_header = 'Код подтверждения для Yamdb'
        message = f'Ваш код подтверждения: {confirmation_code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(
            email_header, message, from_email, [email], fail_silently=False
        )
        return Response(
            {'email': email, 'username': username}, status=status.HTTP_200_OK
        )

    def gettoken(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                'Неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.select_related(
        'category'
    ).prefetch_related(
        'genre'
    ).annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesCreateSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesReadSerializer
        return TitlesCreateSerializer


class ReviewGenreModelMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoriesViewSet(ReviewGenreModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ReviewGenreModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
