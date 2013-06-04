# ************** ERP - TASKS APP - VIEWS ********************* #
from tasks.models import Task
from tasks.forms import IntraTaskForm, CrossTaskForm

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from django.template import RequestContext

from misc.utilities import core_check, core_or_supercoord_check





"""
PROPOSED/TODO:
1. TO ALSO AUTOMATE THE SETTING OF CHILD TASK.

2. ______VERY IMPORTANT____ : AUTOMATICALLY POPULATE THE TASKFORCE FIELDS IN THE EDIT VIEW FOR THE FORM.

5. Also look below for more TODOs
"""



# _____________--- INTRADEPARTMENTAL TASK ADD VIEW ---______________#
"""
MORE INFO:
Can be created/edited by both Supercoords and Cores

Fields entered by user:
    'deadline', 'subject', 'description', 'taskforce', 'parenttask'

Fields automatically taken care of by model/model save function override:
    'taskcreator', 'datecreated', 'datelastmodified', 'depthlevel'

Fields taken care of by the view:
    'targetsubdepts', 'origindept', 'targetdept', 'isxdepartmental', 'taskstatus'
"""
@login_required
@user_passes_test (core_or_supercoord_check)
def add_intra_task(request):


    userprofile = request.user.get_profile()
    department = userprofile.dept
    title = "Add Intradepartmental Task"
    
    if request.method == 'POST':
        form = IntraTaskForm(department, request.POST)
        if form.is_valid():
            newTask = form.save(commit=False)

            #Set the origin & target departments & approve the task.        
            newTask.origindept = userprofile.dept
            newTask.targetdept = userprofile.dept
            newTask.taskcreator = userprofile
            newTask.taskstatus = 'O'
            
            #For many to many relationships to be created, the object MUST first exist in the database.
            newTask.save()
            #UNCOMMENT THE BELOW LINE IF MANYTOMANY DATA IS BEING SAVED DIRECTLY FROM THE FORM
            #form.save_m2m()
                    
            #Get the TaskForce from the form
            cores = form.cleaned_data['cores']
            coords = form.cleaned_data['coords']
            supercoords = form.cleaned_data['supercoords']
            
            #Set the TaskForce for the Task
            for user in coords: 
                newTask.taskforce.add(user)
            for user in supercoords: 
                newTask.taskforce.add(user)
            for user in cores: 
                newTask.taskforce.add(user)
        
            newTask.save()        
            return HttpResponse ("Task Saved")
        else:
            return render_to_response ('tasks/task.html', {'form': form, 'title':title }, context_instance=RequestContext(request))
    
    else:
        form = IntraTaskForm(department)
        context = {'form': form, 'title':title }
        return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))




# _____________--- UNIFIED TASK EDIT VIEW ---______________#
"""
MORE INFO:

INTRADEPARTMENTAL TASKS:
Can be created/edited by both Supercoords and Cores

Fields edited by user:
    'deadline', 'subject', 'description', 'taskforce', 'parenttask', 

Fields automatically taken care of by model/model save function override:
    'datelastmodified', 'depthlevel'

FIELDS THAT WON'T CHANGE:
    'origindept', 'targetdept', 'isxdepartmental', 'taskstatus', 'taskcreator', 'datecreated'

FIELDS THAT ARE GOING TO BE HAVE TO WIPED OUT AND RECREATED:
    'targetsubdepts'
    
    
CROSSDEPARTMENTAL TASKS:
MORE INFO:
Cores ONLY

Fields entered by user:
    'deadline', 'subject', 'description', 'parenttask', 'targetsubdepts'

Fields automatically taken care of by model/model save function override:
    'taskcreator', 'datecreated', 'datelastmodified', 'depthlevel'

Fields taken care of by the view:
    'targetdept'
    
FIELDS THAT WON'T CHANGE:
    'origindept', 'isxdepartmental', 'taskstatus', 'taskcreator', 'datecreated'
    
Fields that are unset:
     'taskforce'
"""
@login_required
@user_passes_test (core_or_supercoord_check)
def edit_task(request, primkey):
    task = Task.objects.get(pk=primkey)
    userprofile = request.user.get_profile()
    department = userprofile.dept

#___________----INTRADEPARTMENTAL TASK EDIT----__________________
    if ((task.isxdepartmental == False) and (task.origindept == department)):
        title = "Edit Intradepartmental Task"
        if request.method == 'POST':
            form = IntraTaskForm(department, request.POST, instance=task)
            if form.is_valid():
                form.save()
                        
                #Get the TaskForce from the form
                cores = form.cleaned_data['cores']
                coords = form.cleaned_data['coords']
                supercoords = form.cleaned_data['supercoords']
                
                #Set the TaskForce for the Task
                task.taskforce.clear()
                
                for user in coords: 
                    task.taskforce.add(user)
                for user in supercoords: 
                    task.taskforce.add(user)
                for user in cores: 
                    task.taskforce.add(user)

                task.save()        
                return HttpResponse ("Task Saved")
            else:
                #Render the form along with all its errors.
                return render_to_response ('tasks/task.html', {'form': form, 'title':title  }, context_instance=RequestContext(request))
        
        else:
            form = IntraTaskForm(department, instance=task)
            context = {'form': form, 'title':title }
            return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))
            
#___________----CROSSDEPARTMENTAL TASK EDIT----__________________

#TODO: 
#For the target core's beenfit, display the ASSIGNED SUBDEPARTMENT in the Approval Page.
#As of now, he has the freedom to assign the task to users from other subdepartments too.

    elif (task.isxdepartmental == True) and (core_check(request.user)):
        if request.method == 'POST':
            #For the originating department's core
            if (task.taskstatus == 'U') and (task.origindept == department):
                title = "Edit Crossdepartmental Task"
                info = "Allowed only until approved by the target department's core."
                form = CrossTaskForm(department, request.POST, instance=task)
                if form.is_valid():
                    form.save()
              
                    #Set the Target Department        
                    for subdept in task.targetsubdepts.all():
                        task.targetdept = subdept.dept
                
                    task.save()
                    return HttpResponse ("Task Saved")
                else:
                    #Render the form again with all its errors.
                    return render_to_response ('tasks/task.html', {'form': form, 'title':title, 'info': info  }, context_instance=RequestContext(request))
            
            #For the target department's core:
            if task.targetdept == department:
                #Getting the targetsubdept. There is only one. The loop will run only once.
                for subdept in task.targetsubdepts:
                    targetsubdept = subdept
                title = "Edit/Approve Crossdepartmental Task"
                info = "Submitting the task here automatically approves & assigns it to the selected workforce.\n<b>Target Subdepartment Requested for the Task: " + targetsubdept + "</b>"
                form = IntraTaskForm(department, request.POST, instance=task)
                if form.is_valid():
                    form.save()
                
                    #Get the TaskForce from the form
                    cores = form.cleaned_data['cores']
                    coords = form.cleaned_data['coords']
                    supercoords = form.cleaned_data['supercoords']
                    
                    #Set the TaskForce for the Task
                    task.taskforce.clear()
                    
                    for user in coords: 
                        task.taskforce.add(user)
                    for user in supercoords: 
                        task.taskforce.add(user)
                    for user in cores: 
                        task.taskforce.add(user)
                    
                    #Approve the task.
                    task.taskstatus = 'O'

                    task.save()        
                    return HttpResponse ("Task Saved/Approved.")
                else:
                    #Render the form again with all its errors.
                    return render_to_response ('tasks/task.html', {'form': form, 'title':title , 'info': info  }, context_instance=RequestContext(request))
            
            else:
                return HttpResponse ("Pack.")
                
        else:
            #For the originating department's core
            if (task.taskstatus == 'U') and (task.origindept == department):
                title = "Edit Crossdepartmental Task"
                info = "Allowed only until approved by the target department's core."
                form = CrossTaskForm (department, instance=task)
                context = {'form': form, 'title':title , 'info': info }
                return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))
            
            #For the target department's core:
            if task.targetdept == department:
                #Getting the targetsubdept. There is only one. The loop will run only once.
                for subdept in task.targetsubdepts:
                    targetsubdept = subdept
                title = "Edit/Approve Crossdepartmental Task"
                info = "Submitting the task here automatically approves & assigns it to the selected workforce.\n<b>Target Subdepartment Requested for the Task: " + targetsubdept + "</b>"
                form = IntraTaskForm(department, instance=task)
                context = {'form': form, 'title':title , 'info': info }
                return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))
                
            else:
                return HttpResponse ("Pack.")

    else: 
        return HttpResponse ("Pack.")
    

        


# _____________--- CROSS DEPARTMENTAL TASK ADD VIEW ---______________#
"""
CORES ONLY


MORE INFO:
Fields entered by user:
    'deadline', 'subject', 'description', 'parenttask', 'targetsubdepts'

Fields automatically taken care of by model/model save function override:
    'taskcreator', 'datecreated', 'datelastmodified', 'depthlevel'

Fields taken care of by the view:
    'origindept', 'targetdept', 'isxdepartmental', 'taskstatus' 
    
Fields that are unset:
     'taskforce'
"""
@login_required
@user_passes_test (core_check)
def add_cross_task(request):
    title = "Add Cross-departmental Task."
    info = "Subject to approval of the target department's core."
    
    userprofile = request.user.get_profile()
    department = userprofile.dept
    
    if request.method == 'POST':
        form = CrossTaskForm(department, request.POST)
        if form.is_valid():
            #Create a task object without writing to the database
            newTask = form.save(commit=False)
            
            #Get selected subdepartment from form and set targetdepartment
            #There's only one object in the form field - the loop is only going to run once.
            for subdept in form.cleaned_data['targetsubdepts']:
                newTask.targetdept = subdept.dept
            
            #Set these variables - Unapproved X-Departmental task
            newTask.taskcreator = userprofile
            newTask.isxdepartmental = True
            newTask.taskstatus = 'U'
      
            #Set the origin & target departments.        
            newTask.origindept = userprofile.dept
            
            #For many to many relationships to be created, the object MUST first exist in the database
            #Saves newTask and also saves the ManyToMany Data
            newTask.save()
            form.save_m2m()
            
            return HttpResponse ("Task Saved")
        else:
            #Render the form again with all its errors.
            return render_to_response ('tasks/task.html', {'form': form, 'title':title, 'info':info  }, context_instance=RequestContext(request))
    else:
        form = CrossTaskForm (department)
        context = {'form': form, 'title':title, 'info':info }
        return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))
        
        



# _____________--- TASK DISPLAY VIEW ---______________#
@login_required
def display_task(request, primkey):

#TODO: Redirect people who aren't allowd to view this task. Add edit and delete buttons for cores and supercoords
#Display ALL details in the template - template needs work.

    try:
        task = Task.objects.get(pk = primkey)
    except:
        return HttpResponse ("That task does not exist.")
    return render_to_response('tasks/display.html', locals() )


# _____________--- TASK DELETE VIEW ---______________#
"""
CORES ONLY
"""
@login_required
@user_passes_test (core_check)
def delete_task(request, primkey):
    try:
        task = Task.objects.get(pk = primkey)
    except:
        return HttpResponse ("That task does not exist.")
    
    task.delete()
    return HttpResponse ("Task Deleted")
    
#TODO: WRITE CODE.

