from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse

from .models import Book, Category


# Rota inicial - mostragem de livros disponíveis
def home(request):
    # Filtrando livros
    query = request.GET.get("q") if request.GET.get("q") != None else ""
    books = Book.objects.filter(
        Q(category__name__icontains=query)
        | Q(title__icontains=query)
        | Q(price__icontains=query)
    )

    categories = Category.objects.all()

    res = {
        "books": books,
        "books_avaliable": books.count(),
        "categories": categories,
        "query": query,
    }

    return render(request, "home.html", res)


# Rota de venda - vender um livro para o cliente

# Rota de cadastro de livros

# Rota de edição de livros

# Rota de histórico de vendas
