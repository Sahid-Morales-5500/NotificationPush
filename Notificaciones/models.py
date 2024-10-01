from django.db import models

# Create your models here.
class PushSuscription(models.Model):
    endpoint = models.URLField()
    keys = models.JSONField()

    def __str__(self):
        return self.endpoint