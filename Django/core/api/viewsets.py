from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import (
    ReadBookSerializer,
    SaleSerializer,
    UserSerializer,
    WriteBookSerializer,
)  # noqa
from ..models import Book, Sale


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ("title", "author_name", "category__name")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadBookSerializer
        return WriteBookSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return SaleSerializer
        raise PermissionDenied("Essa ação não é permitida.")

    @action(detail=True, methods=["get"])
    def user(self, request, pk=None):
        seller = get_object_or_404(User, username=pk)
        sales = Sale.objects.filter(seller=seller)
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def billing(self, request):
        billing = []
        sales = Sale.objects.all()
        for sale in sales:
            billing.append(sale.book.price)

        return Response({"faturamento": sum(billing)})
