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
    """ViewSets/CRUD para o model de Usuários"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action != "create":
            self.permission_classes = [
                IsAuthenticated
            ]  # Precisa estar logado para ver/editar/deletar um usuário
        return super().get_permissions()


class BookViewSet(ModelViewSet):
    """ViewSets/CRUD para o model de Livros"""

    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]  # Filtros de busca
    search_fields = (
        "title",
        "author_name",
        "category__name",
    )  # Campos do filtro # noqa

    def get_serializer_class(self):
        # Define qual serializer será usado de acordo com a ação
        if self.action in ("list", "retrieve"):
            return ReadBookSerializer
        return WriteBookSerializer


class SaleViewSet(ModelViewSet):
    """ViewSets/CRUD para o model de Vendas"""

    queryset = Sale.objects.all()

    def get_serializer_class(self):
        # Não é possivel criar, editar ou deletar uma venda
        if self.action in ("list", "retrieve"):
            return SaleSerializer
        # se não for list ou retrieve, não tem serializer
        raise PermissionDenied("Essa ação não é permitida.")

    def get_permissions(self):
        """Define quais permissões serão usadas de acordo com a ação"""
        if self.action == "billing":
            self.permission_classes = [
                IsAdminUser,
            ]  # Precisa ser admin para ver o faturamento
        else:
            self.permission_classes = [
                IsAuthenticated,
            ]  # Precisa estar logado para as outras ações
        return super().get_permissions()

    @action(detail=True, methods=["get"])
    def user(self, request, pk=None):
        """Retorna as vendas de um usuário específico"""
        seller = get_object_or_404(User, username=pk)
        sales = Sale.objects.filter(seller=seller)
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def billing(self, request):
        """Retorna o faturamento total da livraria **Somente admin**"""
        billing = []
        sales = Sale.objects.all()
        for sale in sales:
            billing.append(sale.book.price)

        return Response({"faturamento": sum(billing)})
