from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import permissions

from ..models import Favourites, Video, User

from ..serializers.VideoSerializer import VideoSerializer


class FavoritesListVideosView(APIView):
    """Список избранного видео"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        video_id = Favourites.objects.filter(user=user).values_list('id', flat=True)
        videos = Video.objects.filter(pk__in=video_id)
        serialized = VideoSerializer(videos, many=True)
        return Response(serialized.data, status=201)


class AddFavoritesVideoView(APIView):
    """Добавление видео в избранное"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, video_id: int):
        video = Video.objects.filter(pk=video_id).first()
        if video is None:
            return Response(status=400)

        user = request.user
        new_favorites = Favourites.objects.create(user=user, video=video)
        new_favorites.save()
        return Response(status=201)

