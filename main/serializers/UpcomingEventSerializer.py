from rest_framework import serializers
from ..models import UpcomingEvent


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingEvent
        fields = "__all__"
