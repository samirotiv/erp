# ERP - DEPTARMENTS APP - MODELS
from django.db import models

# Create your models here.

#Department Model
class dept(models.Model):
    name = models.CharField(max_length=30)

class subdept(models.Model):
    name = models.CharField(max_length=30)
    dept = models.ForeignKey(dept)