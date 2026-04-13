from django.urls import path

from apps.media_test.views.article import (
    ArticleListView,
    ArticleCreateView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
)

app_name = 'media_test'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('articles/<uuid:uuid>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<uuid:uuid>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('articles/<uuid:uuid>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]

