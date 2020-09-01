from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, Post
from .serializers import PostSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    유저의 CRUD API
    
    - id: 유저의 아이디
    - email: 유저의 이메일
    - username: 유저의 유저네임
    - password: 유저의 패스워드
    - first_name: 유저의 성
    - last_name: 유저의 이름
    - last_login: 최근 로그인 날짜
    - date_joined: 회원가입 날짜
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.action in ('create',):
             permission_classes = (AllowAny,)
        elif self.action in ('update', 'partial_update', 'destroy',):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    """
    게시글의 CRUD API

    - title: 게시글 제목
    - content: 게시글의 내용
    - like: 좋아요 수
    - user: 사용자의 id 번호
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    
    def get_permissions(self):
        if self.action in ('list', 'retrieve',):
             permission_classes = (AllowAny,)
        elif self.action in ('create', 'partial_update', 'destroy',):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)  
        return [permission() for permission in permission_classes]
