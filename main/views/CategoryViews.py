from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from ..models import Category, Subcategory

from ..serializers.CategorySerializer import CategorySerializer, SubcategorySerializer, CategoryAndSubcategorySerializer


class CategoryListView(APIView):
    """Список категорий"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        result = CategorySerializer(categories, many=True)
        return Response(result.data, status=200)


class CategoryCreateView(APIView):
    """Создание категории"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.data, status=400)

        serializer.save()
        return Response(status=201)


class SubcategoryListView(APIView):
    """Список подкатегорий категории"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, category_pk):
        category = Category.objects.filter(pk=category_pk).first()
        if category is None:
            return Response(status=400)

        subcategories = Subcategory.objects.filter(category=category)
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=200)


class SubcategoryCreateView(APIView):
    """Создание подкатегории"""

    permission_classes = [permissions.IsAdminUser]

    def post(self, request, category_pk):
        category = Category.objects.filter(pk=category_pk).first()
        if category is None:
            return Response(status=400)

        serializer = SubcategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.data, status=400)

        serializer.save(category=category)
        return Response(serializer.data, status=201)


class SubcategoryAndCategoryView(APIView):
    """Список категорий и подкатегорий для каждой и категорий"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializers = CategoryAndSubcategorySerializer(categories, many=True)
        return Response(serializers.data, status=200)


class UserSubcategories(APIView):
    """Список любимых подкатегорий пользователя"""

    def get(self, request):
        #todo сделать список любимых подкатегорий пользователя. Если их мало - возвращать смежные категории или рандомные
        subcategories = Subcategory.objects.all()
        serialized = SubcategorySerializer(subcategories, many=True)
        return Response(serialized.data, status=200)
