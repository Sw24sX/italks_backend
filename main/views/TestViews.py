from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from djoser import email
from ..models import Category, Subcategory, Video, CategoryNames, SubcategoryNames
from ..serializers.VideoSerializer import VideoSerializer


class TestViews(APIView):
    """Тест"""

    def get(self, request):

        return Response(serializer.data, status=201)

