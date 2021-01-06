from datetime import datetime, date, timedelta

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import  permissions

from ..models import Notifications
from ..serializers.NotificationsSerializer import NotificationsSerializer

from django.core.paginator import Paginator, EmptyPage


class GetNotificationsViews(APIView):
    """Получить список уведомлений"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        notifications = Notifications.objects.filter(user=request.user)
        serialized = NotificationsSerializer(notifications, many=True)
        return Response(serialized.data, status=200)
