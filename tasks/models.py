# ********* ERP - TASKS APP - MODELS ***********

from django.db import models
from users.models import ERPUser
from dept.models import Subdept, Dept
from datetime import date

TASK_STATUSES = ( 
        ( 'U' , 'UNAPPROVED' ) ,
        ( 'O' , 'APPROVED AND ONGOING' ) ,
        ( 'A' , 'APPROVED, ALMOST DONE' ) ,
        ( 'R' , 'REPORTED COMPLETED' ) ,
        ( 'C' , 'COMPLETED' ) ,
        )

class Task(models.Model):
    
    #Central task information
    taskcreator = models.ForeignKey(ERPUser)
    datecreated = models.DateField('Date Created')
    deadline = models.DateField ('Deadline')
    
    #Description of the task
    subject = models.CharField (max_length=100)
    #The following thing should be the model's full-fledged description.
    #As of now, I'm making it a text field, but I think we should
    #put in formatting capability?
    description = models.TextField ( null = True, blank = True )
    
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

    
    
