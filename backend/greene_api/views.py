from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User, Post
from .serializers import PostSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.action == 'create':
             permission_classes = (AllowAny,)
        elif self.action == 'list':
            permission_classes = (IsAdminUser,)
        elif self.action in ('update', 'destroy'):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
