from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,date

# Create your models here.
class Sheet_model(models.Model):
    id= models.IntegerField(default=1,primary_key=True)
    sheet = models.FileField(upload_to='Sheets', blank=False)
    upload_date = models.DateField(auto_now_add=True, blank=False)

