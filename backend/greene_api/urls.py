from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet ,PostViewSet, CommentViewSet, \
     HistoryDestroyViewSet, HashtagGenericViewSet, LikeCreateViewSet

urlpatterns = []

user_router = DefaultRouter()
post_router = DefaultRouter()
history_router = DefaultRouter()
comment_router = DefaultRouter()
hashtag_router = DefaultRouter()
like_router = DefaultRouter()

user_router.register(r'user', UserViewSet, basename='user')
post_router.register(r'tip', PostViewSet, basename='tip')
comment_router.register(r'comment', CommentViewSet, basename='comment')
history_router.register(r'history', HistoryDestroyViewSet, basename='history')
hashtag_router.register(r'hashtag', HashtagGenericViewSet, basename='hashtag')
like_router.register(r'like', LikeCreateViewSet, basename='like')

urlpatterns += user_router.urls
urlpatterns += post_router.urls
urlpatterns += comment_router.urls
urlpatterns += history_router.urls
urlpatterns += hashtag_router.urls
urlpatterns += like_router.urls

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
