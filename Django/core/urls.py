from django.urls import path
from .views import (
    add_book,
    home,
    register_book,
    register_category,
    sale,
    update_book,
)

urlpatterns = [
    path("", home, name="home"),
    path("sale/<str:book_id>", sale, name="sale"),
    path("book/register", register_book, name="register_book"),
    path("book/update/<str:book_id>", update_book, name="update_book"),
    path("book/add/<str:book_id>", add_book, name="add_book"),
    path("category/register", register_category, name="register_category"),
]
