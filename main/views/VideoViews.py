from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions

from ..models import Category, Subcategory, Video

from ..serializers.VideoSerializer import VideoSerializer


class VideoViews(APIView):
    """Информация о видео"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, video_pk):
        video = Video.objects.filter(pk=video_pk).first()
        if video is None:
            return Response(status=400)

        serializer = VideoSerializer(video)
        return Response(serializer.data, status=201)


class VideoCreateView(APIView):
    """Добавить новое видео"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400)

        serializer.save()
        return Response(serializer.data, status=201)


class VideoListCategoryView(APIView):
    """Список видео по категории и подкатегории"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, category_pk):

        category = Category.objects.filter(pk=category_pk).first()
        if category is None:
            return Response(status=400)

        videos = Video.objects.filter(category=category)

        subcategories_name = request.query_params.getlist('subcategories', None)
        if subcategories_name is not None and len(subcategories_name) != 0:
            subcategories = Subcategory.objects.filter(name__in=subcategories_name)
            videos = Video.objects.filter(subcategory__in=subcategories)

        serializer = VideoSerializer(videos.distinct(), many=True)
        return Response(serializer.data, status=201)

class VideosViews(APIView):
    """Видео на главной"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories_name = request.query_params.getlist('categories', None)
        print(categories_name)
        categories = None
        if categories_name is not None and len(categories_name) != 0:
            categories = Category.objects.filter(name__in=categories_name)
        # TODO сделать пагинацию
        videos = Video.objects.all()
        if categories is not None and len(categories) != 0:
            videos = videos.filter(category__in=categories)
        serialized = VideoSerializer(videos.distinct(), many=True)
        return Response(serialized.data, status=201)
