from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import files
# Create your models here.

class customuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)


class saveddata(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    file_name = models.CharField(max_length=100)

