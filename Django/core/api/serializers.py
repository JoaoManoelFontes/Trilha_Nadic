from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    SerializerMethodField,
)
from django.utils.timezone import now

from django.contrib.auth.models import User
from ..models import Book, Category, Sale


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ReadBookSerializer(ModelSerializer):
    category = SlugRelatedField(slug_field="name", read_only=True)
    days_since_created = SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "category",
            "synopsis",
            "author_name",
            "publishing_company_name",
            "release_year",
            "price",
            "quantity",
            "days_since_created",
        ]

    def get_days_since_created(self, obj):
        return "%s days" % (now() - obj.created_at).days


class WriteBookSerializer(ModelSerializer):
    category = CategorySerializer(read_only=False)

    class Meta:
        model = Book
        fields = [
            "title",
            "category",
            "synopsis",
            "author_name",
            "publishing_company_name",
            "release_year",
            "price",
            "quantity",
        ]

    def create(self, validated_data):
        category_data = validated_data["category"]
        try:
            category = Category.objects.get(**category_data)
        except Category.DoesNotExist:
            category = Category.objects.create(**category_data)

        del validated_data["category"]
        book = Book.objects.create(**validated_data, category=category)
        return book


class SaleSerializer(ModelSerializer):
    seller = UserSerializer(read_only=True)
    book = ReadBookSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = ["id", "seller", "book", "client_name"]
