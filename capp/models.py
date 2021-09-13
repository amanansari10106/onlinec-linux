from django.db import models

# Create your models here.
class c_code(models.Model):
    c_code_id = models.AutoField(primary_key=True)
    code = models.TextField()
    