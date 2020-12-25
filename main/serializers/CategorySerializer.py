from rest_framework import serializers

from ..models import Category, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class SubcategorySerializer(serializers.ModelSerializer):
    category_id = serializers.SlugRelatedField(slug_field='id', read_only=True, source='category')

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'category_id')


class SubcategoriesSerializer(serializers.ModelSerializer):
    subcategory_id = serializers.CharField(source='id')
    category_id = serializers.SlugRelatedField(slug_field='id', read_only=True, source='category')

    class Meta:
        model = Subcategory
        fields = ('subcategory_id', 'category_id', 'name')


class CategoryAndSubcategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategoriesSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategory', 'icon_base_64')
