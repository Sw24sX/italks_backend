from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from djoser import email


class TestViews(APIView):
    """Написание поиска"""
    def get(self, request):
        search_request
        return Response(status=201)
