from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Device(models.Model):
    name = models.CharField(max_length=512, null=False)
    user = models.ForeignKey(User, related_name="devices", null=False, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=512, null=False)
    device = models.ForeignKey(Device, related_name="tags", null=False, on_delete=models.CASCADE)
    ratio = models.FloatField(null=False)
    min = models.FloatField(null=False)
    max = models.FloatField(null=False)


class TagValue(models.Model):
    tag = models.ForeignKey(Tag, related_name="tag_values", null=False, on_delete=models.CASCADE)
    value = models.FloatField(null=False)
    timestamp = models.DateTimeField(null=False)
    version = models.CharField(max_length=512, null=False)
