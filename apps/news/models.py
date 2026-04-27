from django.contrib.auth import get_user_model
from django.db import models

from apps.shared.models import BaseModel, Media

User = get_user_model()


class News(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.OneToOneField(
        Media, on_delete=models.CASCADE,
        related_name='news'
    )
    status = models.BooleanField(default=False)

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='news'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
