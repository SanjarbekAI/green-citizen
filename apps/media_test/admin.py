from django.contrib import admin

from apps.media_test.models.article import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail', 'created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    ordering = ('-created_at',)

