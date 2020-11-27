from datetime import datetime, date, timedelta

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
        # todo добавить сортировку
        period = request.query_params.get('period')
        print(period)
        if period == "year":
            current_year_videos = Video.objects.filter(date__lt=self.get_date_start_current_month()) \
                .filter(date__gte=self.get_date_start_current_year())
            serialized_result = VideoSerializer(current_year_videos, many=True)
        elif period == "month":
            current_month_videos = Video.objects.filter(date__lt=self.get_date_start_week()) \
                .filter(date__gte=self.get_date_start_current_month())
            serialized_result = VideoSerializer(current_month_videos, many=True)
        elif period == "week":
            current_week_videos = Video.objects.filter(date__gte=self.get_date_start_week())
            serialized_result = VideoSerializer(current_week_videos, many=True)
        else:
            return Response(status=400)

        return Response(serialized_result.data, status=201)

    @staticmethod
    def get_date_start_week():
        current_date = datetime.now()
        return current_date - timedelta(days=current_date.weekday())

    @staticmethod
    def get_date_start_current_month():
        current_date = datetime.now()
        return current_date - timedelta(days=current_date.day - 1)

    @staticmethod
    def get_date_start_current_year():
        current_date = datetime.now()
        return date(current_date.year, 1, 1)
