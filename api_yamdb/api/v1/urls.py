from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewsViewSet,
    TitlesViewSet,
    UserViewSet,
    SignupViewSet,
)


app_name = 'v1'

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitlesViewSet)
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)
auth_urls = [
    path('signup/', SignupViewSet.as_view(
        {'post': 'signup'}
    ), name='signup'),
    path('token/', SignupViewSet.as_view(
        {'post': 'gettoken'}
    ), name='token'),
]
urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls)),
]
