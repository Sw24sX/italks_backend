from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from ..models import UpcomingEvent
from ..serializers import UpcomingEventSerializer


class EventListView(APIView):
    """Список предстоящих событий"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        events = UpcomingEvent.objects.all()
        serialized = UpcomingEventSerializer.EventListSerializer(events, many=True)
        return Response(serialized.data, status=201)
