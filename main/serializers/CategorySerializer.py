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


class SubcategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name')


class CategoryAndSubcategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategoriesSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategory', 'icon_base_64')
