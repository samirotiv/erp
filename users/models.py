 # ************* ERP - USERS APP - MODELS *************
from django.db import models
from django.contrib.auth.models import User
from dept.models import Dept, Subdept

# Create your models here.


#Annoying little details
HOSTEL_CHOICES  =(
                  ("Ganga", "Ganga"),
                  ("Mandak", "Mandak"),
                  ("Jamuna", "Jamuna"),
                  ("Alak", "Alak"),
                  ("Saraswathi", "Saraswathi"),
                  ("Narmada", "Narmada"),
                  ("Godav", "Godav"),
                  ("Pampa", "Pampa"),
                  ("Tambi", "Tambi"),
                  ("Sindhu", "Sindhu"),
                  ("Mahanadi", "Mahanadi"),
                  ("Sharavati", "Sharavati"),
                  ("Krishna", "Krishna"),
                  ("Cauvery", "Cauvery"),
                  ("Tapti", "Tapti"),
                  ("Brahmaputra", "Brahmaputra"),
                  ("Sarayu", "Sarayu"),
                  )


#User Profile Model
class ERPUser(models.Model):
    user = models.OneToOneField(User)
    dept = models.ForeignKey(Dept, related_name='dept_user_set')
    subdept = models.ForeignKey(Subdept, blank=True, null=True, default=None, related_name='subdept_user_set')

#I think instead of focussing on multiple identities as a specific case, we should take that
#as the general case, of which single identity is a special case.
#About why I'm changing the Foreign Keys above: Django DB will throw errors if you have
#two different relationship fields to the same model. Moreover, it is redundant.
#Hence I've added core_relations as a ForeignKey below ( since a core is always one core of one department )
#I've temporarily only commented out the above lines for clarity. Delete them off after you've understood.
    
    
#<SAMIR>
# I've given this a lot of thought - I didn't say this, but I had always intended to take multiple identities as the general case.
# It makes sense to let the above two fields be since they tell you WHICH identity the user is assuming currently.
# By taking out the above two lines, you won't know what the user is logged into.
# This is going to be a problem unless you want to create a unified login - where a user sees information from all his accounts.
# I have considered this - I conclude it's going to be more painful since a user may be a supercoord of two subdepts - in which case
# for every little thing we'll have to worry about what Identity he wants to use. eg. Create a task as a Supercoord of which department?
#
# I'm changing it back to the original model for the time being. We'll discuss further in the evening if necessary.
#
# It should be a lot easier just to allow the user to assume multiple identies instead of creating a unified dashboard
# So we need those fields. 
# It's fine if the core_relations remain, just in case.
#
# And about the Django Error - that is taken care of by related_name
# </SAMIR>
    
    
    #Handling the Multiple Identity Problem
    multiple_ids = models.BooleanField(default=False)
    coord_relations = models.ManyToManyField(Subdept, related_name='coord_set')
    supercoord_relations = models.ManyToManyField(Dept, related_name='supercoord_set')
    core_relations = models.ForeignKey(Dept, related_name='core_set')

    #Other information
    nickname = models.CharField(max_length=30, blank=True)
    chennai_number = models.CharField(max_length=15, blank=True)
    summer_number = models.CharField(max_length=15, blank=True)
    summer_stay = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True)
    room_no = models.IntegerField(default=0, blank=True)


