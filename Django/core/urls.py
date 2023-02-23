from django.urls import path
from .views import add_book, home, register_book, sale

urlpatterns = [
    path("", home, name="home"),
    path("sale/<str:book_id>", sale, name="sale"),
    path("book/register", register_book, name="register"),
    path("book/add/<str:book_id>", add_book, name="add_book"),
]
