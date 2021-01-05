from datetime import datetime, date, timedelta
from enum import Enum, auto

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import generics, permissions

from ..models import Category, Subcategory, Video, FavoritesCategory, FavoritesSubcategory, ProgressVideoWatch, LastWatchVideo

from ..serializers.VideoSerializers import VideoSerializer

from django.core.paginator import Paginator, EmptyPage


class VideoViews(APIView):
    """Информация о видео"""

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request, video_src: str):
        video = Video.objects.filter(src=video_src).first()
        if video is None:
            return Response(status=400)

        values_for_update = {'video': video}
        if not request.user.is_anonymous:
            obj, created = LastWatchVideo.objects.update_or_create(user=request.user, defaults=values_for_update)

        serializer = VideoSerializer(video, context={'user': request.user})
        return Response(serializer.data, status=201)


class VideoCreateView(APIView):
    """Добавить новое видео"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # todo not implemented

        serializer = VideoSerializer(data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            return Response(status=400)

        serializer.save()
        return Response(serializer.data, status=201)


class VideoPeriod(Enum):
    WEEK = auto()
    MONTH = auto()
    YEAR = auto()


class VideoParameters:
    page: str
    page_size: str
    category_id: int
    subcategory_id: int
    period: str
    order_by: str
    category: Category
    subcategory: Subcategory

    def __init__(self, request: Request, default_page_size=10):
        self.page = request.query_params.get('page', 1)

        self.page_size = request.query_params.get('page_size', default_page_size)

        self.category_id = request.query_params.get('category_id', None)
        if self.category_id is not None:
            self.category_id = int(self.category_id)

        self.subcategory_id = request.query_params.get('subcategory_id', None) #todo
        if self.subcategory_id is not None:
            self.subcategory_id = int(self.subcategory_id)

        self.period = request.query_params.get('period', None)
        if self.period is not None and self.period not in ["year", "month", "week"]:
            raise ValueError("period can only be a 'year' | 'month' | 'week'")

        self.order_by = request.query_params.get('order_by', None)
        if self.order_by is not None:
            if self.order_by not in ["name", "new_date", "old_date", "duration"]:
                raise ValueError("order_by can only be a 'name' | 'new_date' | 'old_date' | 'duration'")
            elif self.order_by == 'new_date':
                self.order_by = "-date"
            elif self.order_by == 'old_date':
                self.order_by = 'date'
        self.subcategory = None
        self.category = None

    def subcategory_id_and_category_id_is_correct(self):
        if self.category_id_is_exists() and self.subcategory_id_is_exists():
            return Subcategory.objects.filter(pk=self.subcategory_id, category_id=self.category_id).exists()
        return False

    def category_id_is_exists(self):
        if self.category_id is not None:
            return Category.objects.filter(pk=self.category_id).exists()
        return False

    def subcategory_id_is_exists(self):
        if self.subcategory_id is not None:
            return Subcategory.objects.filter(pk=self.subcategory_id).exists()
        return False

    def find_category(self) -> bool:
        self.category = Category.objects.filter(pk=self.category_id).first()
        return self.category is not None

    def find_subcategory(self) -> bool:
        self.subcategory = Subcategory.objects.filter(pk=self.subcategory_id).first()
        return self.subcategory is not None


class VideoListCategoryView(APIView):
    """Список видео по категории и подкатегории"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, category_pk):
        # todo сделать сортировку безопасной
        if not Category.objects.filter(pk=category_pk).exists():
            return Response({'error': "Category with entered category_id was not found"}, status=400)

        try:
            video_params = VideoParameters(request, default_page_size=60)
        except (ValueError, TypeError) as error:
            return Response({'error': error.__str__()}, status=400)

        videos = VideosViews.get_videos_by_period(video_params.period)
        videos = videos.filter(category__id=category_pk)

        if video_params.subcategory_id is not None:
            videos = videos.filter(subcategory__id=video_params.subcategory_id)
        if video_params.order_by is not None:
            videos = videos.order_by(video_params.order_by)

        if video_params.page_size is None:
            video_params.page_size = 60
        videos, paginator = VideosViews.get_videos_page(videos, video_params.page, video_params.page_size)

        serialized_result = VideoSerializer(videos, many=True, context={'user': request.user})
        data = {
            "is_last_page": int(video_params.page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized_result.data
        }
        return Response(data, status=201)


class PromoVideoViews(APIView):
    """Promo videos"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            video_params = VideoParameters(request, default_page_size=6)
        except (ValueError, TypeError) as error:
            return Response(status=400)
        if video_params.find_category() and video_params.find_subcategory() \
                and not video_params.subcategory_id_and_category_id_is_correct():
            return Response(status=400)

        user = request.user
        data = {
            "week": self.get_serialized_list_videos('week', video_params, user),
            "month": self.get_serialized_list_videos('month', video_params, user),
            "year": self.get_serialized_list_videos('year', video_params, user),
        }

        if video_params.category is not None:
            data['category_name'] = video_params.category.name
            if not request.user.is_anonymous:
                data['category_is_favorite'] = FavoritesCategory.objects.filter(user=request.user,
                                                                                category=video_params.category).exists()

        if video_params.subcategory is not None:
            data['subcategory_name'] = video_params.subcategory.name
            if not request.user.is_anonymous:
                data['subcategory_is_favorite'] = FavoritesSubcategory.objects.filter(user=request.user,
                                                                                      subcategory=video_params.subcategory).exists()
        return Response(data, status=200)

    def get_filtered_videos_by_period(self, period: str, video_params: VideoParameters):
        videos = VideosViews.get_videos_by_period(period)
        if video_params.category_id is not None:
            videos = videos.filter(category__id=video_params.category_id)
        if video_params.subcategory_id is not None:
            videos = videos.filter(subcategory__id=video_params.subcategory_id)
        return videos

    def get_serialized_list_videos(self, period: str, video_params, user):
        videos = self.get_filtered_videos_by_period(period, video_params)
        videos, _ = VideosViews.get_videos_page(videos, video_params.page, video_params.page_size)
        return VideoSerializer(videos, many=True, context={'user': user}).data


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

        # todo добавить обработку исключений
        page = request.query_params.get('page')
        if order_by is not None:
            videos = videos.order_by(order_by)
        videos, paginator = self.get_videos_page(videos, page)
        if videos is None:
            return Response(status=400)

        serialized_result = VideoSerializer(videos, many=True, context={'user': request.user})
        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized_result.data
        }
        # TODO ЗАМЕНИТЬ НА СТАТУС 200 ВЕЗДЕ
        return Response(data, status=200)

    @staticmethod
    def get_videos_page(videos, page, page_size=60):
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
        videos = Video.objects.all()
        if period == "year":
            # ONLY FOR DEV
            pk_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            videos = videos.filter(pk__in=pk_list)
            #videos = videos.filter(date__lt=self.get_date_start_current_month()) \
            #    .filter(date__gte=self.get_date_start_current_year())
        elif period == "month":
            pk_list = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            videos = videos.filter(pk__in=pk_list)
            #videos = videos.filter(date__lt=self.get_date_start_week()) \
            #    .filter(date__gte=self.get_date_start_current_month())
        elif period == "week":
            #pk_list = [i for i in range(1, 122)]
            videos = Video.objects.all()
            #videos = videos.filter(date__gte=self.get_date_start_week())
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


class SimilarVideosViews(APIView):
    """Список похожих видео"""

    def get(self, request, video_src):
        # todo запоминать данные о видео, его категорию и тд
        video = Video.objects.filter(src=video_src).first()
        if video is None:
            return Response(status=400)

        page = request.query_params.get('page')
        if page is None:
            return Response({'error': "Page not specified"})

        page_size = request.query_params.get('page_size')
        if page_size is None:
            page_size = 10

        category = video.category.all()
        subcategory = video.subcategory.all()

        to_few_videos = 5
        videos = Video.objects.filter(subcategory__in=subcategory).order_by('-date')
        videos_count = videos.count()
        if videos_count < to_few_videos:
            videos = videos | Video.objects.filter(category__in=category).order_by("-date")

        paginator = Paginator(videos, page_size)
        videos = paginator.page(page)
        result = VideoSerializer(videos, many=True, context={'user': request.user})

        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": result.data
        }

        return Response(data, status=200)


class SaveProgressWatchVideoView(APIView):
    """Сохранение прогресса просмотра видео (в секундах)"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, video_id):
        video = Video.objects.filter(pk=video_id).first()
        if video is None:
            return Response({'error': "Video not found"}, status=400)

        time_per_seconds = request.query_params.get('time', None)
        if time_per_seconds is None:
            return Response({'error': "Time not found"}, status=400)

        try:
            time_per_seconds = int(time_per_seconds)
        except ValueError as error:
            return Response({'error': error.__str__()}, status=400)

        values_for_update = {'time': time_per_seconds}
        obj, created = ProgressVideoWatch.objects.update_or_create(user=request.user,
                                                                   video=video, defaults=values_for_update)
        video = Video.objects.filter(pk=obj.video.pk).first()
        serialized = VideoSerializer(video, context={'user': request.user})
        return Response(serialized.data, status=202)


class LastWatchVideoView(APIView):
    """Последнее просмотренное видео"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        video_id = LastWatchVideo.objects.filter(user=request.user).values_list('id', flat=True).first()
        video = Video.objects.filter(pk=video_id).first()
        serialized = VideoSerializer(video, context={'user': request.user})
        return Response(serialized.data, status=200)
