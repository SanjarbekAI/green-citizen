from rest_framework import serializers

from apps.news.models import News
from apps.shared.mixins.read_mixin import TranslatedFieldsReadMixin


class NewsListSerializer(TranslatedFieldsReadMixin, serializers.ModelSerializer):
    translatable_fields = ['title', 'content']
    media_fields = ['image']

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'created_at']
