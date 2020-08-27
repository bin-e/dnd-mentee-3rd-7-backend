from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="GreenE API",
      default_version='v1',
      description=
      '''
      # Open API 문서 페이지

      ### 기본 사용법
      1. 사용자 생성
      **[POST] {host}/api/user/**

      2. JWT Token 획득
      **[POST] {host}/token/**

      3. JWT Token 추가 
      **swagger --> Authorrize 버튼 클릭 후 Bearer {Token} 등록**
      **postman --> header에 Authorization: Bearer {Toekn} 등록**

      ### 권한
      1. Anonymous
      2. Staff
      3. Admin
 
      ''',
      contact=openapi.Contact(email="ljh9032a@naver.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('greene_api.urls')),
]

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

