from django.urls import path, include

from .views import (CategoryViews, SearchViews, FavoritesViews, UserView, TestViews,
                    VideoViews, UpcomingEventViews, NotificationsViews)


urlpatterns = [
    path('categories_and_subcategories/', CategoryViews.SubcategoryAndCategoryView.as_view()),
    path('category/', CategoryViews.CategoryCreateView.as_view()),
    path('category/<int:category_pk>/', CategoryViews.SubcategoryListView.as_view()),
    path('category/<int:category_pk>/create-subcategory/', CategoryViews.SubcategoryCreateView.as_view()),

    path('subcategory/user/', CategoryViews.UserSubcategories.as_view()),

    path('video/', VideoViews.VideosViews.as_view()),
    path('video/info/<str:video_src>/', VideoViews.VideoViews.as_view()),  # Подробная информация о видео
    #path('video/<int:video_id>/', VideoViews.VideoViews.as_view()),
    #path('video/create/', VideoCreateView.as_view()),
    path('video/sorted/<int:category_pk>/', VideoViews.VideoListCategoryView.as_view()),  # Список видео по категории
    path('video/promo/', VideoViews.PromoVideoViews.as_view()),
    path('video/similar/<str:video_src>/', VideoViews.SimilarVideosViews.as_view()),  # Список похожих видео
    path('video/time/<int:video_id>/', VideoViews.SaveProgressWatchVideoView.as_view()),  # Сохранение прогресса просмотра видео (в секундах)
    path('video/last/', VideoViews.LastWatchVideoView.as_view()),  # Получение последнего просмотренного видео

    path('auth/check_token/', UserView.CheckToken.as_view()),

    path('search/', SearchViews.Search.as_view()),

    path('favorites/video/', FavoritesViews.FavoritesListVideosView.as_view()),  # Список избранных видео
    path('favorites/video/add/<int:video_id>/', FavoritesViews.AddFavoritesVideoView.as_view()),  # Добавление видео в избранное
    path('favorites/video/remove/<int:video_id>/', FavoritesViews.RemoveFavoritesVideoView.as_view()),  # Удаление видео из избранного
    path('favorites/subcategory/', FavoritesViews.FavoritesListSubcategoryViews.as_view()),  # спиок отслеживаемых категорий
    path('favorites/subcategory/add/<int:subcategory_id>/', FavoritesViews.FavoritesAddSubcategoryView.as_view()),  # добавление подкатегории в отслеживаемое
    path('favorites/subcategory/remove/<int:subcategory_id>/', FavoritesViews.FavoritesRemoveSubcategoryView.as_view()),  # удаление подкатегории из отслеживаемого
    path('favorites/category/add/<int:category_id>/', FavoritesViews.FavoritesAddCategoryViews.as_view()),  # добавление категории в избранное
    path('favorites/category/remove/<int:category_id>/', FavoritesViews.FavoritesRemoveCategoryViews.as_view()),  # удаление категорий из избранного

    path('events/', UpcomingEventViews.EventListView.as_view()),

    path('settings/', UserView.Settings.as_view()),  # Получениие данных настроек пользователя
    path('settings/user/', UserView.UserSettingsView.as_view()),  # Сохранение изменений данных пользователя
    path('settings/other/', UserView.OtherSettingsView.as_view()),
    path('settings/notification/<int:is_notification>/', UserView.NotificationsSettingsView.as_view()),  # Изменение флага "получать уведомления"
    path('settings/dark_theme/<int:is_dark_theme>/', UserView.DarkThemeSettingsView.as_view()),  # Изменение флага "темная тема"
    path('settings/as_device/<int:is_as_device>/', UserView.AsDeviceSettingsView.as_view()),  # Изменение флага "как на устройстве"

    path('notifications/', NotificationsViews.GetNotificationsViews.as_view()),

    path('test/', TestViews.TestViews.as_view()),

]
