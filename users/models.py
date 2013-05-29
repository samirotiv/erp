 # ERP - USERS APP - MODELS
from django.db import models
from django.contrib.auth.models import User
from erp.dept.models import dept, subdept

# Create your models here.

#User Profile Model
class ERPUser(models.Model):
    user = models.OneToOneField(User)
    dept = models.ForeignKey(dept)
    subdept = models.ForeignKey(subdept, blank=True, null=True, default=None)

    #Handling the Multiple Identity Problem
    multiple_ids = models.BooleanField(default=False)
    coord_relations = models.ManyToManyField(subdept)
    supercoord_relations = models.ManyToManyField(dept)

    #Other information
    nickname = models.CharField(max_length=30, blank=True)
    chennai_number = models.CharField(max_length=15, blank=True)
    summer_number = models.CharField(max_length=15, blank=True)
    summer_stay = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True)
#PLEASE PASTE THE HOSTEL_CHOICES LIST
    room_no = models.IntegerField(default=0, blank=True)