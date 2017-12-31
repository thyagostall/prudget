from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.code
