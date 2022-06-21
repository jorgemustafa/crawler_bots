from django.db import models


class SkinData(models.Model):
    weapon = models.CharField(max_length=100, null=True, blank=True)
    gold = models.TextField(null=True, blank=True)
    blue = models.TextField(null=True, blank=True)
    urls = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.weapon


class SkinLog(models.Model):
    weapon = models.CharField(max_length=100, null=True, blank=True)
    gold = models.TextField(null=True, blank=True)
    blue = models.TextField(null=True, blank=True)
    urls = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.weapon
