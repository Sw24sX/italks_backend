from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from ..models import Video, CategoryNames, SubcategoryNames
from ..serializers.VideoSerializers import VideoSerializer
from django.core.paginator import Paginator, EmptyPage


class Search(APIView):
    """Поиск (первая версия)"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search_request = request.GET.get('query', None)
        if search_request is None:
            return Response(status=400)
        list_search = [i.lower() for i in search_request.split()]
        #videos_by_category = self._get_videos_by_categories(list_search)
        #videos_by_subcategory = self._get_videos_by_subcategories(list_search)
        videos_by_name = self._get_videos_by_name(search_request)
        #videos = videos_by_category.union(videos_by_subcategory, videos_by_name)
        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
        if page_size is None:
            page_size = 60

        order_by = request.query_params.get('order_by')  # name, new_date, old_date, duration
        if order_by == "new_date":
            order_by = "-date"
        elif order_by == "old_date":
            order_by = "date"
        videos = videos_by_name.order_by(order_by)

        videos, paginator = self.get_videos_page(videos, page, page_size)

        serialized = VideoSerializer(videos, many=True, context={'user': request.user})
        data = {
            "is_last_page": int(page) == paginator.num_pages,
            "number_pages": paginator.num_pages,
            "count": paginator.count,
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

    def _get_videos_by_categories(self, list_search: list):
        categories_id = CategoryNames.objects \
            .filter(name__in=list_search) \
            .values_list('category_id', flat=True) \
            .distinct()
        videos = Video.objects.filter(subcategory__category_id__in=categories_id).distinct()
        return videos

    def _get_videos_by_subcategories(self, list_search: list):
        subcategories_id = SubcategoryNames.objects \
            .filter(name__in=list_search) \
            .values_list('subcategory_id', flat=True) \
            .distinct()
        videos = Video.objects.filter(subcategory__id__in=subcategories_id).distinct()
        return videos

    def _get_videos_by_name(self, search):
        videos = Video.objects.filter(name__istartswith=search).distinct()
        return videos
