from django.shortcuts import render
from django.http import HttpResponse

from .models import Book


# Rota inicial - mostragem de livros disponíveis
def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})


# Roda de venda - vender um livro para o cliente

# Rota de cadastro de livros

# Rota de edição de livros

# Rota de histórico de vendas
