from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from ..models import Video, CategoryNames, SubcategoryNames
from ..serializers.VideoSerializer import VideoSerializer


class Search(APIView):
    """Поиск (первая версия)"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search_request = request.GET.get('query', None)
        if search_request is None:
            return Response(status=400)
        list_search = [i.lower() for i in search_request.split()]
        videos_by_category = self._get_videos_by_categories(list_search)
        videos_by_subcategory = self._get_videos_by_subcategories(list_search)
        videos_by_name = self._get_videos_by_name(search_request)
        videos = videos_by_category.union(videos_by_subcategory, videos_by_name)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=201)

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
