from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings


class TestViews(APIView):
    """Тестовый get запрос (отправка письма)"""
    def get(self, request):
        send_mail(
            'Subject here',
            'Here is the message.',
            settings.EMAIL_HOST_PASSWORD,
            ['aleksandr.korolyov.99@mail.ru'],
            fail_silently=False,
        )
        return Response(status=201)
