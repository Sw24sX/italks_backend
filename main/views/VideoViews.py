from datetime import datetime, date, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions

from ..models import Category, Subcategory, Video

from ..serializers.VideoSerializer import VideoSerializer

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage


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
        # todo добавить сортировку
        period = request.query_params.get('period')
        subcategory_id = request.query_params.get('subcategory')

        videos = VideosViews.get_videos_by_period(period)
        if videos is None:
            return Response(status=400)

        videos = videos.filter(category__id=category_pk)
        if subcategory_id is not None:
            videos = videos.filter(subcategory__id=subcategory_id)

        # todo добавить обработку исключений; попробовать использовать annotate
        #page_size = request.query_params.get('page_size')
        page_size = 10
        paginator = Paginator(videos, page_size)
        page = request.query_params.get('page')
        try:
            videos = paginator.page(page)
        except EmptyPage:
            return Response(status=400)
        except:
            return Response(status=400)

        serialized_result = VideoSerializer(videos, many=True)
        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized_result.data
        }
        return Response(data, status=201)



class VideosViews(APIView):
    """Видео на главной"""

    permission_classes = [permissions.AllowAny]
    #pagination_class = PaginationVideo

    def get(self, request):
        # todo добавить сортировку
        period = request.query_params.get('period')
        videos = self.get_videos_by_period(period)
        if videos is None:
            return Response(status=400)

        # todo добавить обработку исключений; попробовать использовать annotate
        #page_size = request.query_params.get('page_size')
        page_size = 6
        paginator = Paginator(videos, page_size)
        page = request.query_params.get('page')
        try:
            videos = paginator.page(page)
        except EmptyPage:
            return Response(status=400)
        except:
            return Response(status=400)
        serialized_result = VideoSerializer(videos, many=True)
        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized_result.data
        }
        return Response(data, status=201)

    @staticmethod
    def get_videos_by_period(period: str):
        if period == "year":
            # ONLY FOR DEV
            pk_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            videos = Video.objects.filter(pk__in=pk_list)
            #videos = Video.objects.filter(date__lt=self.get_date_start_current_month()) \
            #    .filter(date__gte=self.get_date_start_current_year())
        elif period == "month":
            pk_list = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            videos = Video.objects.filter(pk__in=pk_list)
            #videos = Video.objects.filter(date__lt=self.get_date_start_week()) \
            #    .filter(date__gte=self.get_date_start_current_month())
        elif period == "week":
            #pk_list = [i for i in range(1, 122)]
            videos = Video.objects.all()
            #videos = Video.objects.filter(date__gte=self.get_date_start_week())
        else:
            return None
        return videos

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
