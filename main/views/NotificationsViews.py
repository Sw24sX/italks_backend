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


class GetCountNotificationsViews(APIView):
    """Получить количество непрочитанных уведомлений"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        notifications_count = Notifications.objects.filter(user=request.user).count()
        data = {
            'notifications_count': notifications_count
        }
        return Response(data, status=200)


class NotificationsViews(APIView):
    """Полная информация об уведомлениях (список + количество уведомлений)"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        notifications = Notifications.objects.filter(user=request.user)
        serialized = NotificationsSerializer(notifications, many=True)
        data = {
            'count': notifications.count(),
            'notifications': serialized.data
        }

        return Response(data, status=200)


class MarkAsReadNotificationsView(APIView):
    """Пометить список уведомлений как прочитанные"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        from_id = request.query_params.get('from', None)
        to_id = request.query_params.get('to', None)
        notifications = Notifications.objects.filter(user=request.user)

        if from_id is not None:
            notifications = notifications.filter(pk__gte=from_id)
        if to_id is not None:
            notifications = notifications.filter(pk__lte=to_id)

        serialised = NotificationsSerializer(notifications, many=True).data
        notifications.delete()
        return Response(serialised, status=200)
