from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions

from ..models import Category, Subcategory, Video

from ..serializers.VideoSerializer import VideoSerializer


class VideoViews(APIView):
    """Информация о видео"""

    #permission_classes = [permissions.IsAuthenticated]

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
    """Список видео по категории и подкатегории"""

    def get(self, request, category_pk):

        category = Category.objects.filter(pk=category_pk).first()
        if category is None:
            return Response(status=400)

        videos = Video.objects.filter(category=category)

        subcategories_id = request.query_params.getlist('subcategories', None)
        if subcategories_id is None or len(subcategories_id) != 0:
            subcategories = Subcategory.objects.filter(name__in=subcategories_id)
            videos = Video.objects.filter(subcategory__in=subcategories)

        serializer = VideoSerializer(videos.distinct(), many=True)
        return Response(serializer.data, status=201)
