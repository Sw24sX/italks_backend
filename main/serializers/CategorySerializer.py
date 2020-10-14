from rest_framework import serializers

from ..models import Category, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Subcategory
        fields = "__all__"
