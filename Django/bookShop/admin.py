from django.contrib import admin

# Register your models here.
from .models import Category, Book, Sale

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Sale)
