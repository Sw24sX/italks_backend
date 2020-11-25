from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken import serializers, views
from rest_framework.authentication import TokenAuthentication


class CheckToken(APIView):
    """Проверка на актуальность токена"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(status=201)
