from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from djoser import email
from ..models import Category, Subcategory, Video, NameCategoryForSearch


class TestViews(APIView):
    """Написание поиска"""
    def get(self, request):
        search_request = request.GET.get('query', None)
        if search_request is None:
            return Response(status=400)
        list_search = search_request.split()
        videos_by_category = self._get_videos_by_categories(list_search)
        print("####")
        for i in videos_by_category:
            print(i)
        print("####")
        return Response(status=201)

    def _get_videos_by_categories(self, list_search):
        category_names = NameCategoryForSearch.objects\
            .filter(name__in=list_search)\
            .values_list('category_id', flat=True)\
            .distinct()
        category = Category.objects.filter(pk__in=category_names).values_list('id', flat=True)
        videos = Video.objects.filter(subcategory__category_id__in=category).distinct()
        return videos

