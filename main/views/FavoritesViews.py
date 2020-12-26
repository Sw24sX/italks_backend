from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import permissions
from django.core.paginator import Paginator, EmptyPage

from ..models import FavouritesVideos, Video, User, FavoritesCategory, Category, Subcategory, FavoritesSubcategory

from ..serializers.VideoSerializer import VideoSerializer
from ..serializers.CategorySerializer import CategorySerializer, SubcategoriesSerializer


class FavoritesListVideosView(APIView):
    """Список избранного видео"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        video_id = FavouritesVideos.objects.filter(user=user).values_list('id', flat=True)
        videos = Video.objects.filter(pk__in=video_id)

        order_by = request.query_params.get('order_by')  # name, new_date, old_date, duration
        if order_by == "new_date":
            order_by = "-date"
        elif order_by == "old_date":
            order_by = "date"
        if order_by is not None:
            videos = videos.order_by(order_by)

        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
        if page_size is None:
            page_size = 60
        videos, paginator = self.get_videos_page(videos, page, page_size)

        serialized = VideoSerializer(videos, many=True, context={'user': request.user})

        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized.data
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


class AddFavoritesVideoView(APIView):
    """Добавление видео в избранное"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, video_id: int):
        video = Video.objects.filter(pk=video_id).first()
        if video is None:
            return Response(status=400)

        user = request.user
        try:
            FavouritesVideos.objects.create(user=user, video=video).save()
        except:
            return Response({'error': "Video has already been added"}, status=400)

        return Response(status=201)


class RemoveFavoritesVideoView(APIView):
    """Удаление видео из избранного"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, video_id: int):
        video = FavouritesVideos.objects.filter(video_id=video_id, user=request.user)
        if video.first() is None:
            return Response(status=400)

        video.delete()
        return Response(status=200)


class FavoritesListSubcategoryViews(APIView):
    """Список отслеживаемых категорий"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        categories_list_id = FavoritesCategory.objects.filter(user=user).values_list('category_id', flat=True)
        categories = Category.objects.filter(pk__in=categories_list_id)
        serialized_categories = CategorySerializer(categories, many=True)

        subcategories_list_id = FavoritesSubcategory.objects.filter(user=user).values_list('subcategory_id', flat=True)
        subcategories = Subcategory.objects.filter(pk__in=subcategories_list_id)
        serialized = SubcategoriesSerializer(subcategories, many=True)
        return Response(serialized.data, status=201)


class FavoritesAddCategoryViews(APIView):
    """Добавление категории в отслеживаемое"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, category_id):
        user = request.user
        category = Category.objects.filter(pk=category_id).first()
        if category is None:
            return Response(status=400)

        #TODO Сделать нормальную обработку ошибок
        try:
            FavoritesCategory.objects.create(user=user, category=category).save()
        except:
            return Response(status=400)

        for subcategory in category.subcategory.all():
            try:
                FavoritesSubcategory.objects.create(user=user, subcategory=subcategory).save()
            except:
                continue

        return Response(status=201)


class FavoritesRemoveCategoryViews(APIView):
    """Удаление категории из избранного"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, category_id):
        user = request.user
        favorite_category = FavoritesCategory.objects.filter(category_id=category_id)
        if favorite_category.first() is None:
            return Response(status=400)

        favorite_category.delete()
        favorite_subcategories = FavoritesSubcategory.objects.filter(subcategory__category_id=category_id)
        favorite_subcategories.delete()

        return Response(status=200)


class FavoritesAddSubcategoryView(APIView):
    """Добавление подкатегории в отслеживаемое"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, subcategory_id):
        user = request.user
        subcategory = Subcategory.objects.filter(pk=subcategory_id).first()
        if subcategory is None:
            return Response(status=400)

        # TODO Сделать нормальную обработку ошибок
        try:
            FavoritesSubcategory.objects.create(user=user, subcategory=subcategory).save()
        except:
            return Response(status=400)

        return Response(status=201)
