from django.db import models

# Create your models here.
# core/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='login_logs')
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=True)
    token_used = models.CharField(max_length=255, blank=True) # To track which token was used

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "User Login Log"
        verbose_name_plural = "User Login Logs"

    def __str__(self):
        return f"{self.user if self.user else 'Anonymous'} - {self.timestamp} ({'Success' if self.successful else 'Failed'})"