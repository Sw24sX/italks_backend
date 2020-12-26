from django.urls import path, include

from .views import (CategoryViews, SearchViews, FavoritesViews, UserView, TestViews, VideoViews, UpcomingEventViews)


urlpatterns = [
    path('categories_and_subcategories/', CategoryViews.SubcategoryAndCategoryView.as_view()),
    path('category/', CategoryViews.CategoryCreateView.as_view()),
    path('category/<int:category_pk>/', CategoryViews.SubcategoryListView.as_view()),
    path('category/<int:category_pk>/create-subcategory/', CategoryViews.SubcategoryCreateView.as_view()),

    path('subcategory/user/', CategoryViews.UserSubcategories.as_view()),

    path('video/', VideoViews.VideosViews.as_view()),
    path('video/<int:video_pk>/', VideoViews.VideoViews.as_view()),  # Подробная информация о видео
    #path('video/create/', VideoCreateView.as_view()),
    path('video/sorted/<int:category_pk>/', VideoViews.VideoListCategoryView.as_view()),  # Список видео по категории
    path('video/promo/', VideoViews.PromoVideoViews.as_view()),
    path('video/similar/<int:video_id>/', VideoViews.SimilarVideosViews.as_view()),  # Список похожих видео

    path('auth/check_token/', UserView.CheckToken.as_view()),

    path('search/', SearchViews.Search.as_view()),

    path('favorites/video/', FavoritesViews.FavoritesListVideosView.as_view()),  # Список избранных видео
    path('favorites/video/add/<int:video_id>/', FavoritesViews.AddFavoritesVideoView.as_view()),  # Добавление видео в избранное
    path('favorites/subcategory/', FavoritesViews.FavoritesListSubcategoryViews.as_view()),  # спиок отслеживаемых категорий
    path('favorites/subcategory/add/<int:subcategory_id>/', FavoritesViews.FavoritesAddSubcategoryView.as_view()),
    path('favorites/category/add/<int:category_id>/', FavoritesViews.FavoritesAddCategoryViews.as_view()),  # добавление категории в избранное

    path('events/', UpcomingEventViews.EventListView.as_view()),

    path('test/', TestViews.TestViews.as_view()),

]
