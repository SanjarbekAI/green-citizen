from django.contrib import admin

from apps.news.models import News
from apps.shared.admin import MyTranslationOption


@admin.register(News)
class NewsAdmin(MyTranslationOption):
    list_display = ['id', 'title', 'status', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['status', 'created_at', 'updated_at']
