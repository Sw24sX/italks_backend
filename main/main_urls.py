from django.urls import path, include

from .views import (CategoryViews, SearchViews, FavoritesViews, UserView, TestViews, VideoViews, UpcomingEventViews)


urlpatterns = [
    path('categories_and_subcategories/', CategoryViews.SubcategoryAndCategoryView.as_view()),
    path('category/', CategoryViews.CategoryListView.as_view()),
    path('category/', CategoryViews.CategoryCreateView.as_view()),
    path('category/<int:category_pk>/', CategoryViews.SubcategoryListView.as_view()),
    path('category/<int:category_pk>/create-subcategory/', CategoryViews.SubcategoryCreateView.as_view()),

    path('video/', VideoViews.VideosViews.as_view()),
    path('video/<int:video_pk>/', VideoViews.VideoViews.as_view()),  # Подробная информация о видео
    #path('video/create/', VideoCreateView.as_view()),
    path('video/sorted/<int:category_pk>/', VideoViews.VideoListCategoryView.as_view()),  # Список видео по категории

    path('auth/check_token/', UserView.CheckToken.as_view()),

    path('search/', SearchViews.Search.as_view()),

    path('favorites_list/', FavoritesViews.FavoritesListVideosView.as_view()),
    path('favorites_add/<int:video_id>/', FavoritesViews.AddFavoritesVideoView.as_view()),

    path('events/', UpcomingEventViews.EventListView.as_view()),

    path('test/', TestViews.TestViews.as_view()),

]
