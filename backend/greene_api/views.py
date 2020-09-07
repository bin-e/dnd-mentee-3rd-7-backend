import random 

from django.db.models import Subquery
from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from .models import User, Post, Comment, History, Hashtag, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, HistorySerializer, HashtagSerializer, LikeSerializer, MyTokenObtainPairSerializer
from .swagger_decorators import param_query_hint


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.action in ('create',):
            permission_classes = (AllowAny,)
        elif self.action in ('update', 'partial_update', 'destroy', 'histories', 'posts', 'liked-posts'):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=True, url_path='histories')
    def histories(self, request, pk=None):
        user = self.get_object()
        histories = user.history_set.all()
        top_3_histories = histories.order_by('-id')[:3]
        serializer = HistorySerializer(top_3_histories, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='posts')
    def posts(self, request, pk=None):
        user = self.get_object()
        Posts = user.post_set.all()
        serializer = PostSerializer(Posts, many=True)
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=True, url_path='liked-posts')
    def liked_posts(self, request, pk=None):
        user = self.get_object()
        likes = Like.objects.filter(user=user)
        Posts = Post.objects.filter(id__in=Subquery(likes.values('post')))
        serializer = PostSerializer(Posts, many=True)
        return Response(serializer.data)
        

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    
    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(title__icontains=query)
        return queryset
    
    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'comments'):
            permission_classes = (AllowAny,)
        elif self.action in ('create', 'partial_update', 'destroy',):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)  
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(manual_parameters=[param_query_hint])
    def list(self, request, *args, **kwargs):
        query = self.request.query_params.get('query', None)
        if query is not None and request.user is not None:
            History.objects.create(user=request.user, query=query)
        return super().list(request, *args, **kwargs)
    
    @action(methods=['GET'], detail=True, url_path='comments')
    def comments(self, request, pk=None):
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

    
class HistoryDestroyViewSet(viewsets.GenericViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        history = self.get_object()
        user = User.objects.get(id=history.user.id)
        self.perform_destroy(history)
        
        histories = user.history_set.all()
        top_3_histories = histories.order_by('-id')[:3]
        serializer = HistorySerializer(top_3_histories, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.delete()


class HashtagGenericViewSet(viewsets.GenericViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = None
    
    @action(methods=['GET'], detail=False, url_path='recommend-hashtags')
    def recommend_hashtags(self, request):
        queryset = self.get_queryset()
        queryset_k = random.choices(queryset, k=3)
        serializer = self.get_serializer(queryset_k, many=True)
        return Response(serializer.data)


class LikeCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
