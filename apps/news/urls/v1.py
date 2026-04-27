from django.urls import path

from apps.news.views.detail import NewsRetrieveAPIView
from apps.news.views.list import NewsListAPIView

app_name = 'news'

urlpatterns = [
    # check if phone number exists, send code and give tokens
    path('', NewsListAPIView.as_view(), name='list'),
    path('<int:pk>/', NewsRetrieveAPIView.as_view(), name='detail'),
]
