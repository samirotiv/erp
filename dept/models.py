# ************ ERP - DEPTARMENTS APP - MODELS *****************
from django.db import models

# Create your models here.

#Department Model
class Dept(models.Model):
    name = models.CharField(max_length=30)

class Subdept(models.Model):
    name = models.CharField(max_length=30)
    dept = models.ForeignKey(Dept)