from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from djoser import email


class TestViews(APIView):
    """Тестовый get запрос (отправка письма)"""
    def get(self, request):
        a = getattr(settings, 'DOMAIN', '')
        print(a)
        return Response(status=201)
