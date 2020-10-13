from django.urls import path, include
from .views.UserViews import UserAuthView, UserView, UserDataView
from .views.CategoryViews import CategoryView, SubcategoryView


urlpatterns = [
    path('user_auth/', UserAuthView.as_view()),
    path('user/', UserView.as_view()),
    path('user_data/', UserDataView.as_view()),

    path('category/', CategoryView.as_view()),
    path('subcategory/<int:category_pk>/', SubcategoryView.as_view()),
]
