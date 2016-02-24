from django.db import models
from django.utils.translation import ugettext_lazy as _


class LogInAttempt(models.Model):

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('log in attempt')
        verbose_name_plural = _('log in attempts')

    def __str__(self):
        return self.username
