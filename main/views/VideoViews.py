from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Category, Subcategory, Video

from ..serializers.VideoSerializer import VideoSerializer\


class VideoViews(APIView):
    """Информация о видео"""
    def get(self, request, video_pk):
        video = Video.objects.filter(pk=video_pk).first()
        if video is None:
            return Response(status=400)

        serializer = VideoSerializer(video)
        return Response(serializer.data, status=201)


class VideoCreateView(APIView):
    """Добавить новое видео"""
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400)

        serializer.save()
        return Response(serializer.data, status=201)


class VideoListCategoryView(APIView):
    """Список видео по категории"""
    def get(self, request, category_pk):
        #todo повышение беопасности
        videos = Video.objects.filter(category_id=category_pk)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=201)


class VideoListSubcategoryView(APIView):
    """Список видео по подкатегории"""
    def get(self, request, category_pk, subcategory_pk):
        #todo повышение беопасности
        subcategory = Subcategory.objects.filter(pk=subcategory_pk).first()
        videos = subcategory.video_set.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=201)