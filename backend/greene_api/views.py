import random 

from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User, Post, Comment, History, Hashtag
from .serializers import UserSerializer, PostSerializer, CommentSerializer, HistorySerializer, HashtagSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    유저의 CRUD API
    
    - id: 유저의 아이디
    - email: 유저의 이메일
    - username: 유저의 유저네임
    - password: 유저의 패스워드
    - name: 유저의 이름
    - last_login: 최근 로그인 날짜
    - date_joined: 회원가입 날짜
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.action in ('create',):
             permission_classes = (AllowAny,)
        elif self.action in ('update', 'partial_update', 'destroy', 'histories_of_user',):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['GET'])
    def histories_of_user(self, request, pk=None):
        user = self.get_object()
        histories = user.history_set.all()
        top_3_histories = histories.order_by('-id')[:3]
        serializer = HistorySerializer(top_3_histories, many=True)
        return Response(serializer.data)
        

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
    
    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(title__icontains=query)
        return queryset
    
    param_query_hint = openapi.Parameter(
        'query',
        openapi.IN_QUERY,
        description='A sting that be filtered on list of posts',
        type=openapi.TYPE_STRING
    )
    
    @swagger_auto_schema(manual_parameters=[param_query_hint])
    def list(self, request, *args, **kwargs):
        query = self.request.query_params.get('query', None)
        if query is not None and request.user is not None:
            History.objects.create(user=request.user, query=query)
        return super().list(request, *args, **kwargs)
    
    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'comments_of_post'):
             permission_classes = (AllowAny,)
        elif self.action in ('create', 'partial_update', 'destroy',):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)  
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['GET'])
    def comments_of_post(self, request, pk=None):
        post = self.get_object()
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.action in ('retrieve'):
             permission_classes = (AllowAny,)
        elif self.action in ('create', 'partial_update', 'destroy',):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,) 
        return [permission() for permission in permission_classes]

    
class HistoryDestroyModelViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


class HashtagGenericViewSet(viewsets.GenericViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = None
    
    @action(detail=False, methods=['GET'])
    def recommend_hashtags(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset_k = random.choices(queryset, k=3)
        serializer = self.get_serializer(queryset_k, many=True)
        return Response(serializer.data)
    