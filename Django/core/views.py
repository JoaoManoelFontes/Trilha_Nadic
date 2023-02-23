from django.shortcuts import redirect, render
from django.db.models import Q

# from django.http import HttpResponse

from .forms.book_form import BookForm

from .models import Book, Category, Sale


def home(request):
    """Rota da página inicial"""

    # Filtrando livros
    query = request.GET.get("q") if request.GET.get("q") is not None else ""
    books = Book.objects.filter(
        Q(category__name__icontains=query)
        | Q(title__icontains=query)
        | Q(price__icontains=query)
    )

    # Obtendo todas as categorias
    categories = Category.objects.all()

    # Construindo o dicionário da response
    response = {
        "books": books,
        "books_avaliable": books.count(),
        "categories": categories,
        "query": query,
    }

    return render(request, "home.html", response)


def sale(request, book_id):
    """Rota de venda de livros"""

    # Obtendo as informações do livro em questão
    book = Book.objects.get(pk=book_id)

    if request.method == "POST":
        # Diminuindo a quantidade de livros disponíveis
        book.quantity -= 1
        book.save()
        # Cadastrando uma nova venda com os dados passados pelo POST
        client_name = request.POST["client"]
        sale = Sale(seller=request.user, book=book, client_name=client_name)
        sale.save()
        # Redirecionando para a página inicial
        return redirect("home")

    return render(request, "sale.html", {"book": book})


def add_book(request, book_id):
    """Rota de adição de livros existentes"""
    book = Book.objects.get(pk=book_id)
    book.quantity += int(request.GET.get("quantity"))
    book.save()
    return redirect("home")


def register_book(request):
    """Rota de cadastro de livros"""
    if request.method == "POST":
        book = BookForm(request.POST)
        if book.is_valid():
            book.save()
            return redirect("home")
    return render(request, "book_form.html", {"form": BookForm()})


# Rota de edição de livros

# Rota de histórico de vendas
