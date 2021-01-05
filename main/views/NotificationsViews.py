from datetime import datetime, date, timedelta

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import generics, permissions

from ..models import Category, Subcategory, Video, FavoritesCategory, FavoritesSubcategory, ProgressVideoWatch, LastWatchVideo

from ..serializers.VideoSerializer import VideoSerializer

from django.core.paginator import Paginator, EmptyPage


