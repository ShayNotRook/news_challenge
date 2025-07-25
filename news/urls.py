from django.urls import path

from .views import GetAllNews


urlpatterns = [
    path('news', GetAllNews.as_view(), name='get_all_news'),
]