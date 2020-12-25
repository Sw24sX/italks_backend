from datetime import datetime, date, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions

from ..models import Category, Subcategory, Video, FavoritesCategory, FavoritesSubcategory

from ..serializers.VideoSerializer import VideoSerializer

from django.core.paginator import Paginator, EmptyPage


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
        # todo сделать сортировку безопасной

        period = request.query_params.get('period')
        subcategory_id = request.query_params.get('subcategory')
        order_by = request.query_params.get('order_by')  # name, new_date, old_date, duration
        if order_by == "new_date":
            order_by = "-date"
        elif order_by == "old_date":
            order_by = "date"
        videos = VideosViews.get_videos_by_period(period)
        if videos is None:
            return Response(status=400)

        videos = videos.filter(category__id=category_pk)
        if subcategory_id is not None:
            videos = videos.filter(subcategory__id=subcategory_id)
        if order_by is not None:
            videos = videos.order_by(order_by)

        # todo добавить обработку исключений; попробовать использовать annotate
        #page_size = request.query_params.get('page_size')

        page = request.query_params.get('page')
        videos, paginator = VideosViews.get_videos_page(videos, page)

        serialized_result = VideoSerializer(videos, many=True)
        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized_result.data
        }
        return Response(data, status=201)


class PromoVideoViews(APIView):
    """Promo videos"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        category_id = request.query_params.get('category_id')
        category = None
        if category_id is not None:
            category = Category.objects.filter(pk=category_id).first()
            if category is None:
                return Response(status=400)

        subcategory_id = request.query_params.get('subcategory_id')
        subcategory = None
        if subcategory_id is not None:
            subcategory = Subcategory.objects.filter(pk=subcategory_id).first()
            if subcategory is None:
                return Response(status=400)

        page_size = request.query_params.get('page_size')
        if page_size is None:
            page_size = 6
        page = request.query_params.get('page')
        if page is None:
            page = 1

        week_videos = VideosViews.get_videos_by_period('week')
        month_videos = VideosViews.get_videos_by_period('month')
        year_videos = VideosViews.get_videos_by_period('year')

        if subcategory_id is not None:
            week_videos = week_videos.filter(subcategory__id=subcategory_id)
            month_videos = month_videos.filter(subcategory__id=subcategory_id)
            year_videos = year_videos.filter(subcategory__id=subcategory_id)

        if category_id is not None:
            week_videos = week_videos.filter(category__id=category_id)
            month_videos = month_videos.filter(category__id=category_id)
            year_videos = year_videos.filter(category__id=category_id)

        data = {
            "week": self.get_serialized_list_videos(week_videos, page, page_size),
            "month": self.get_serialized_list_videos(month_videos, page, page_size),
            "year": self.get_serialized_list_videos(year_videos, page, page_size),
            'category_is_favorite': False,
            'subcategory_is_favorite': False
        }

        if category_id is not None:
            data['category_name'] = category.name
            if not request.user.is_anonymous:
                data['category_is_favorite'] = FavoritesCategory.objects.filter(user=request.user,
                                                                                category=category).exists()

        if subcategory_id is not None:
            data['subcategory_name'] = subcategory.name
            if not request.user.is_anonymous:
                data['subcategory_is_favorite'] = FavoritesSubcategory.objects.filter(user=request.user,
                                                                                      subcategory=subcategory).exists()
        return Response(data, status=201)

    @staticmethod
    def get_serialized_list_videos(videos, page, page_size):
        videos, _ = VideosViews.get_videos_page(videos, page, page_size)
        return VideoSerializer(videos, many=True).data


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

        order_by = request.query_params.get('order_by')  # name, new_date, old_date, duration
        if order_by == "new_date":
            order_by = "-date"
        elif order_by == "old_date":
            order_by = "date"

        # todo добавить обработку исключений; попробовать использовать annotate
        page = request.query_params.get('page')
        if order_by is not None:
            videos = videos.order_by(order_by)
        videos, paginator = self.get_videos_page(videos, page)
        if videos is None:
            return Response(status=400)


        serialized_result = VideoSerializer(videos, many=True)
        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized_result.data
        }
        return Response(data, status=201)

    @staticmethod
    def get_videos_page(videos, page: int, page_size=60):
        paginator = Paginator(videos, page_size)
        try:
            videos = paginator.page(page)
        except EmptyPage:
            return None, paginator
        except:
            return None, paginator

        return videos, paginator

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
