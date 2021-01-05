from datetime import datetime, timedelta, date

#from Tools.scripts.findlinksto import visit
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from djoser import email
from ..models import Category, Subcategory, Video, CategoryNames, SubcategoryNames, LastWatchVideo
from ..serializers import TestSerializer, VideoSerializers
from django.db.models import Q
import random
import json


class TestViews(APIView):
    """Тест"""

    def post(self, request):
        password = request.data['new_password']
        user = request.user
        user.set_password(password)
        user.save()
        #data = LastWatchVideo.objects.filter(user=request.user, video_id=3).first()
        #print(data)
        #serialized = VideoSerializers.LastVideoSerializer(data)
        return Response( status=201)

    def fill_videos(self):
        videos = Video.objects.filter(pk__gte=30)
        for video in videos:
            category = Category.objects.filter(pk=random.randint(1, 4)).first()
            subcategories = category.subcategory.all()
            video.category.add(category)
            for j in subcategories:
                video.subcategory.add(j)

    def create_many_videos(self):
        videos = Video.objects.all()
        for video in videos:
            new_video = Video.objects.create(
                name=video.name,
                src=video.src,
                author=video.author,
                is_favorite=video.is_favorite,
                duration=video.duration,
                date=video.date,
                resource=video.resource
            )
            new_video.save()
