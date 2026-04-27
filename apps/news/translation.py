from modeltranslation.translator import register, TranslationOptions

from apps.news.models import News


@register(News)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)
