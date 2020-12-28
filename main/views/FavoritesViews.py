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
        video_id = FavouritesVideos.objects.filter(user=user).values_list('video_id', flat=True)
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
        serialized = VideoSerializer(videos, many=True, context={'user': user})

        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "videos_page": serialized.data
        }
        return Response(data, status=200)

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
        video = Video.objects.filter(pk=video_id)
        if video.first() is None:
            return Response(status=400)

        user = request.user
        try:
            FavouritesVideos.objects.create(user=user, video=video.first()).save()
        except:
            return Response({'error': "Video has already been added"}, status=400)

        serialized = VideoSerializer(video, many=True, context={'user': request.user})
        return Response(serialized.data, status=201)


class RemoveFavoritesVideoView(APIView):
    """Удаление видео из избранного"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, video_id: int):
        video = Video.objects.filter(pk=video_id)
        if video.first() is None:
            return Response(status=400)

        favorite_video = FavouritesVideos.objects.filter(video=video.first(), user=request.user)
        if favorite_video.first() is None:
            return Response(status=400)

        favorite_video.delete()

        serialized = VideoSerializer(video, many=True, context={'user': request.user})
        return Response(serialized.data, status=200)


class FavoritesListSubcategoryViews(APIView):
    """Список отслеживаемых подкатегорий"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        subcategories_list_id = FavoritesSubcategory.objects.filter(user=user).values_list('subcategory_id', flat=True)
        subcategories = Subcategory.objects.filter(pk__in=subcategories_list_id)
        serialized = SubcategoriesSerializer(subcategories, many=True)
        return Response(serialized.data, status=200)


class FavoritesAddCategoryViews(APIView):
    """Добавление категории в отслеживаемое"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, category_id):
        category = Category.objects.filter(pk=category_id).first()
        if category is None:
            return Response(status=400)

        #TODO Сделать нормальную обработку ошибок
        try:
            FavoritesCategory.objects.create(user=request.user, category=category).save()
        except:
            return Response(status=400)

        favorite_subcategory_id = FavoritesSubcategory.objects\
            .filter(user=request.user, subcategory__category=category)\
            .values_list('subcategory_id', flat=True)
        subcategories = Subcategory.objects.filter(category=category).exclude(pk__in=favorite_subcategory_id)
        for subcategory in subcategories:
            try:
                FavoritesSubcategory.objects.create(user=request.user, subcategory=subcategory).save()
            except:
                continue

        serialized = SubcategoriesSerializer(subcategories, many=True)
        return Response(serialized.data, status=201)


class FavoritesRemoveCategoryViews(APIView):
    """Удаление категории из избранного"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, category_id):
        user = request.user
        favorite_category = FavoritesCategory.objects.filter(category_id=category_id, user=user)
        if favorite_category.first() is None:
            return Response(status=400)

        favorite_category.delete()
        favorite_subcategories = FavoritesSubcategory.objects.filter(subcategory__category_id=category_id, user=user)
        subcategories_id = list(favorite_subcategories.values_list('subcategory_id', flat=True))
        subcategories = Subcategory.objects.filter(pk__in=subcategories_id)
        favorite_subcategories.delete()
        serialized = SubcategoriesSerializer(subcategories, many=True)

        return Response(serialized.data, status=200)


class FavoritesAddSubcategoryView(APIView):
    """Добавление подкатегории в отслеживаемое"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, subcategory_id):
        user = request.user
        subcategory = Subcategory.objects.filter(pk=subcategory_id)
        if subcategory.first() is None:
            return Response(status=400)

        # TODO Сделать нормальную обработку ошибок
        try:
            FavoritesSubcategory.objects.create(user=user, subcategory=subcategory.first()).save()
        except:
            return Response(status=400)

        serialized = SubcategoriesSerializer(subcategory, many=True)
        return Response(serialized.data, status=201)


class FavoritesRemoveSubcategoryView(APIView):
    """Удаление подкатегории из отслеживаемого"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, subcategory_id):
        user = request.user
        subcategory = Subcategory.objects.filter(pk=subcategory_id)
        if subcategory.first() is None:
            return Response(status=400)

        favorite_subcategory = FavoritesSubcategory.objects.filter(subcategory_id=subcategory_id, user=user)
        if favorite_subcategory.first() is None:
            return Response(status=400)

        favorite_subcategory.delete()
        serialized = SubcategoriesSerializer(subcategory, many=True)

        return Response(serialized.data, status=200)
