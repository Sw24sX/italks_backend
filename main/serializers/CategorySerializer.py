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
    #subcategory = serializers.SlugRelatedField(
    #    many=True,
    #    read_only=True,
    #    slug_field='name__id'
    # )

    subcategory = SubcategoriesSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategory')
