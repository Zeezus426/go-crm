from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Task(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
