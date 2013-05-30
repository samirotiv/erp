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
    
    #This is the task status variable.
    #One question is what it defaults to. This depends on isxdepartmental.
    #TODO: Write a method that handles this.
    taskstatus = models.CharField ( max_length=1, choices=TASK_STATUSES )

    #Task Nesting
    parenttask = models.ForeignKey('self', null=True, blank=True, default=None, related_name='parent_task')
    depthlevel = models.IntegerField(default=0)

    def __unicode__():
        return self.Descr

    def isPastDeadline():
        return date.today() > self.Deadline

    
    
