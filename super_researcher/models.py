from django.db import models

# Create your models here.
class SuperResearcher(models.Model):
    company = models.CharField(max_length=200,null= True)
    website = models.URLField(max_length=200, null= True)
    phone_number = models.IntegerField(null= True)
    email = models.EmailField(max_length=200, null= True)
    full_name = models.CharField(max_length=200, null= True)
    promoted = models.BooleanField(default=False)
    is_active_lead = models.BooleanField(default=False)
