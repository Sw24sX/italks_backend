from datetime import datetime, timedelta, date

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from djoser import email
from ..models import Category, Subcategory, Video, CategoryNames, SubcategoryNames
from ..serializers.VideoSerializer import VideoSerializer
from ..serializers import TestSerializer
from django.db.models import Q


class TestViews(APIView):
    """Тест"""

    def get(self, request):
        video_2 = Video.objects.get(pk=2)
        temp = self.get_date_start_current_month()
        print(temp)
        print(video_2.date)
        current_year_videos = Video.objects.filter(Q(date__gte=self.get_date_start_week()))
        print(current_year_videos)
        serialized_current_year_videos = VideoSerializer(current_year_videos, many=True)
        return Response(serialized_current_year_videos.data, status=201)

    @staticmethod
    def get_date_start_week():
        current_date = datetime.now()
        return current_date - timedelta(days=current_date.weekday())

    @staticmethod
    def get_date_start_current_month():
        current_date = datetime.now()
        return current_date - timedelta(days=current_date.day - 2)

    @staticmethod
    def get_date_start_current_year():
        current_date = datetime.now()
        return date(current_date.year, 1, 1)

