import logging

from django.db import models

from apps.shared.models import BaseModel, Media

logger = logging.getLogger(__name__)


class Article(BaseModel):
    """
    Demo model showing how to use the shared Media model.

    - thumbnail: single image (ForeignKey → Media)
    - gallery: multiple files (ManyToManyField → Media)
    """

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default='')

    # Single media reference (e.g. cover image)
    thumbnail = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='article_thumbnails',
    )

    # Multiple media references (e.g. photo gallery)
    gallery = models.ManyToManyField(
        Media,
        blank=True,
        related_name='article_galleries',
    )

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
