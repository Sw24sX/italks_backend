from django.urls import path, include
from .views.CategoryViews import CategoryView, SubcategoryView, SubcategoryAndCategoryView
from .views.VideoViews import VideoViews, VideoCreateView, VideoListCategoryView
from .views.TestViews import TestViews


urlpatterns = [
    path('categories_and_subcategories/', SubcategoryAndCategoryView.as_view()),
    path('category/', CategoryView.as_view()),
    path('category/<int:category_pk>/', SubcategoryView.as_view()),

    path('video/<int:video_pk>/', VideoViews.as_view()),  # Подробная информация о видео
    #path('video/create/', VideoCreateView.as_view()),
    path('video/sorted/<int:category_pk>/', VideoListCategoryView.as_view()),  # Список видео по категории

    path('test/', TestViews.as_view())
]
