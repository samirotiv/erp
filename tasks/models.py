# ********* ERP - TASKS APP - MODELS ***********

from django.db import models
from users.models import ERPUser
from dept.models import Subdept, Dept
from datetime import date

TASK_STATUSES = ( 
        ( 'U' , 'UNAPPROVED' ) ,
        ( 'O' , 'APPROVED AND ONGOING' ) ,
        ( 'A' , 'APPROVED, ALMOST DONE' ) '
        ( 'C' , 'COMPLETED' )
        )

class Task(models.Model):
    taskcreator = models.ForeignKey(ERPUser)
    datecreated = models.DateField('Date Created')
    deadline = models.DateField ('Deadline')
    descr = models.CharField (max_length=40)
    
    #Group of users doing the task.
    taskforce = models.ManyToManyField (ERPUser, related_name='taskforce')
    
    #Classify tasks by subdepartments to facilitate easy querying.
    targetsubdepts = models.ManyToManyField (Subdept, related_name='targetsubdepts')
    
    #Taking care of cross-departmental tasks.
    origindept = models.ForeignKey(Dept, related_name='origindept')
    targetdept = models.ForeignKey(Dept, related_name='targetdept')
    isxdepartmental = models.BooleanField(default=False)
    
# STILL UNDECIDED - DO WE NEED ALL THESE BOOLEANS? ONE INTEGER/STRING CAN DO THE TRICK.
# MADE ALL OF THEM ANYWAY
# TASKSTATUS KEPT AS INTEGERFIELD
# TODO: VISWA PLEASE SET IT AS YOU LIKE TO A STRING OR WHATEVER SUITS YOU.
    #Task Status
    taskapproved = models.BooleanField(default=False)
    taskcompleted = models.BooleanField(default=False)
    taskstatus = models.IntegerField()

    #Task Nesting
    parenttask = models.ForeignKey('self', null=True, blank=True, default=None, related_name='parent_task')
    depthlevel = models.IntegerField(default=0)

    def __unicode__():
        return self.Descr

    def isPastDeadline():
        return date.today() > self.Deadline

    
    
