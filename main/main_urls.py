from django.urls import path, include
from .views.UserViews import UserAuthView, UserView, UserDataView
from .views.CategoryViews import CategoryView, SubcategoryView
from .views.VideoViews import VideoViews, VideoCreateView, VideoListCategoryView, VideoListSubcategoryView


urlpatterns = [
    path('user_auth/', UserAuthView.as_view()),
    path('user/', UserView.as_view()),
    path('user_data/', UserDataView.as_view()),

    path('category/', CategoryView.as_view()),
    path('subcategory/<int:category_pk>/', SubcategoryView.as_view()),

    path('video/<int:video_pk>/', VideoViews.as_view()),  # Подробная информация о видео
    #path('video/create/', VideoCreateView.as_view()),
    path('video/sorted/<int:category_pk>/', VideoListCategoryView.as_view()),  # Список видео по категории
    path('video/sorted/<int:category_pk>/<int:subcategory_pk>/', VideoListSubcategoryView.as_view())  # Список видео по категории и подкатегории
]
