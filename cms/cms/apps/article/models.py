from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext, gettext_lazy as _


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    summary = models.TextField()
    file = models.FileField()
    categories = ArrayField(models.CharField(max_length=100), size=10, blank=True, null=True)
