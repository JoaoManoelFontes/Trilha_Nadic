from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from .forms.book_form import BookForm
from .forms.category_form import CategoryForm

from .models import Book, Category, Sale
from django.contrib.auth.models import User


@login_required(login_url="/admin/login/?next=/")  # Rota protegida
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


@login_required(login_url="/admin/login/?next=/")
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


@login_required(login_url="/admin/login/?next=/book/register")
def register_book(request):
    """Rota de cadastro de livros"""
    if request.method == "POST":
        # Pegando os dados passados pelo método POST
        book = BookForm(request.POST)
        if book.is_valid():
            # Salvando o livro se ele for válido
            book.save()
            return redirect("home")

        # Retornando o formulário com os erros, se houver
        return render(
            request,
            "book_form.html",
            {"form": BookForm(), "errors": book.errors},
        )

    return render(request, "book_form.html", {"form": BookForm()})


@login_required(login_url="/admin/login/?next=/category/register")
def register_category(request):
    """Rota de cadastro de categorias"""
    if request.method == "POST":
        # Pegando os dados passados pelo método POST
        category = CategoryForm(request.POST)
        if category.is_valid():
            # Salvando o livro se ele for válido
            category.save()
            return redirect("register_book")
    return render(request, "category_form.html", {"form": CategoryForm()})


def update_book(request, book_id):
    """Rota de edição de livros (parecida com a rota de cadastro))"""
    book = Book.objects.get(pk=book_id)
    if request.method == "POST":
        book_form = BookForm(request.POST, instance=book)
        if book_form.is_valid():
            book_form.save()
            return redirect("home")

        return render(
            request,
            "book_form.html",
            {"form": BookForm(instance=book), "errors": book_form.errors},
        )

    return render(
        request,
        "book_form.html",
        {"form": BookForm(instance=book)},
    )


def delete_book(request, book_id):
    """Rota de exclusão de livros"""
    book = Book.objects.get(pk=book_id)
    book.delete()
    return redirect("home")


@login_required(login_url="/admin/login/?next=/sales/")
def sales_history(request):
    """Rota de histórico de vendas"""
    if request.GET.get("seller") is not None:
        # Obtendo o usuário e filtrando as vendas dele
        user = get_object_or_404(User, username=request.GET.get("seller"))
        sales = Sale.objects.filter(seller=user)
    else:
        # Obtendo todas as vendas
        sales = Sale.objects.all()

    # Calculando o valor total das vendas (em geral ou de um usuário)
    billing = sales.values_list("book__price", flat=True)

    return render(request, "sales.html", {"sales": sales, "billing": sum(billing)})
