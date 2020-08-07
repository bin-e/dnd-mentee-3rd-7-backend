from rest_framework.response import Response

from .serializers import UserCreateSerializer
from rest_framework import generics, status


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'A user is created'}, status=status.HTTP_201_CREATED, headers=headers)
