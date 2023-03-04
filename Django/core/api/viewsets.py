from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .serializers import ReadBookSerializer, UserSerializer, WriteBookSerializer  # noqa
from ..models import Book


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadBookSerializer
        return WriteBookSerializer
