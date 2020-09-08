from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    UserViewSet,
    PostViewSet, 
    CommentViewSet,
    HistoryDestroyViewSet, 
    HashtagGenericViewSet, 
    LikeCreateViewSet,
    MyTokenObtainPairView,
    FileCreateViewSet,
)

urlpatterns = []

user_router = DefaultRouter(trailing_slash=False)
post_router = DefaultRouter(trailing_slash=False)
history_router = DefaultRouter(trailing_slash=False)
comment_router = DefaultRouter(trailing_slash=False)
hashtag_router = DefaultRouter(trailing_slash=False)
like_router = DefaultRouter(trailing_slash=False)
file_router = DefaultRouter(trailing_slash=False)

user_router.register(r'user', UserViewSet, basename='user')
post_router.register(r'tip', PostViewSet, basename='tip')
comment_router.register(r'comment', CommentViewSet, basename='comment')
history_router.register(r'history', HistoryDestroyViewSet, basename='history')
hashtag_router.register(r'hashtag', HashtagGenericViewSet, basename='hashtag')
like_router.register(r'like', LikeCreateViewSet, basename='like')
file_router.register(r'file', FileCreateViewSet, basename='file')

urlpatterns += user_router.urls
urlpatterns += post_router.urls
urlpatterns += comment_router.urls
urlpatterns += history_router.urls
urlpatterns += hashtag_router.urls
urlpatterns += like_router.urls
urlpatterns += file_router.urls

urlpatterns += [
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
