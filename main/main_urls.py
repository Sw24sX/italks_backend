from django.urls import path, include
from .views.UserViews import UserAuthView, UserView, UserDataView


urlpatterns = [
    path('user_auth/', UserAuthView.as_view()),
    path('user/', UserView.as_view()),
    path('user_data/', UserView.as_view()),
]
