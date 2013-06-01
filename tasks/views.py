# ************** ERP - TASKS APP - VIEWS *********************
from tasks.models import Task
from tasks.forms import IntraTaskForm, CrossTaskForm

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404

from django.template import RequestContext

#UNNECESSARY: ONLY FOR TESTING.
from dept.models import Dept 


# _____________--- CORE CHECK FUNCTION ---______________#
def core_check (user):
    loginuser = user.get_profile()
    return loginuser.status == 2


"""
PROPOSED/TODO:
TO ALSO AUTOMATE THE SETTING OF CHILD TASK.
"""



# _____________--- INTRADEPARTMENTAL TASK ADD VIEW ---______________#
"""
MORE INFO:
Fields entered by user:
    'deadline', 'subject', 'description', 'taskforce', 'parenttask'

Fields automatically taken care of by model/model save function override:
    'taskcreator', 'datecreated', 'datelastmodified', 'depthlevel'

Fields taken care of by the view:
    'targetsubdepts', 'origindept', 'targetdept', 'isxdepartmental', 'taskstatus'
"""
#@login_required
#@user_passes_test (core_check)
def add_intra_task(request):

#TODO: UNCOMMENT WHEN THE LOGIN SYSTEM IS READY 
    #userprofile = request.user.get_profile()
    #department = userprofile.dept
#TESTING LINE: REMOVE WHEN LOGIN SYSTEM IS READY
    department = Dept.objects.get(pk='1')
    
    if request.method == 'POST':
        form = IntraTaskForm(department, request.POST)
        if form.is_valid():
            newTask = form.save()
        
#TODO: UNCOMMENT COMMENTS WHEN THE LOGIN SYSTEM IS READY 
            #newTask.taskcreator = userprofile
        
            #Set these variables - Approved & Ongoing Intra-departmental task.
            newTask.isxdepartmental = False
            newTask.taskstatus = 'O'
            
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
        
#TODO: UNCOMMENT WHEN THE LOGIN SYSTEM IS READY        
            #Set the origin & target departments.        
            #newTask.origindept = userprofile.dept
            #newTask.targetdept = userprofile.dept
            
            # Add the concerned subdepartments to the "targetsubdepts" field.
            for user in coords:
                for usersubdept in user.coord_relations.all():
                    if usersubdept.dept == newTask.origindept:
                        newTask.targetsubdepts.add(usersubdept)
        
            newTask.save()
        
            return HttpResponse ("Task Saved")
        else:
            return render_to_response ('tasks/task.html', {'form': form }, context_instance=RequestContext(request))
    
    else:
        form = IntraTaskForm(department)
        context = {'form': form}
        return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))


# _____________--- INTRADEPARTMENTAL TASK EDIT VIEW ---______________#
"""
MORE INFO:
Fields edited by user:
    'deadline', 'subject', 'description', 'taskforce', 'parenttask', 

Fields automatically taken care of by model/model save function override:
    'datelastmodified', 'depthlevel'

FIELDS THAT WON'T CHANGE:
    'origindept', 'targetdept', 'isxdepartmental', 'taskstatus', 'taskcreator', 'datecreated'

FIELDS THAT ARE GOING TO BE HAVE TO WIPED OUT AND RECREATED:
    'targetsubdepts'
"""
#@login_required
#@user_passes_test (core_check)
def edit_intra_task(request, primkey):
    if request.method == 'POST':
        form = IntraTaskForm(request.POST)
        if form.is_valid():
            newTask = form.save()
        
#TODO: REMOVE THE COMMENTS WHEN THE LOGIN SYSTEM IS READY 
            #userprofile = request.user.get_profile()
            #newTask.taskcreator = userprofile
        
            #Set these variables - Approved & Ongoing Intra-departmental task.
            newTask.isxdepartmental = False
            newTask.taskstatus = 'O'
        
#TODO: REMOVE THE COMMENTS WHEN THE LOGIN SYSTEM IS READY        
            #Set the origin & target departments.        
            #newTask.origindept = userprofile.dept
            #newTask.targetdept = userprofile.dept
            
            # Add the concerned subdepartments to the "targetsubdepts" field.
            newTask.populateTargetSubdepts()
        
            newTask.save()
        
            return HttpResponse ("Task Saved")
        else:
            return render_to_response ('tasks/task.html', {'form': form }, context_instance=RequestContext(request))
    
    else:
        form = IntraTaskForm()
        context = {'form': form}
        return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))        
        
        
        


# _____________--- CROSS DEPARTMENTAL TASK ADD VIEW ---______________#
"""
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
#@login_required
#@user_passes_test (core_check)
def add_cross_task(request):

#TODO: UNCOMMENT WHEN THE LOGIN SYSTEM IS READY 
    #userprofile = request.user.get_profile()
    #department = userprofile.dept
#TESTING LINE: REMOVE WHEN LOGIN SYSTEM IS READY
    department = Dept.objects.get(pk='1')
    
    if request.method == 'POST':
        form = CrossTaskForm(department, request.POST)
        if form.is_valid():
            newTask = form.save()
        
#TODO: UNCOMMENT WHEN THE LOGIN SYSTEM IS READY 
            #userprofile = request.user.get_profile()
            #newTask.taskcreator = userprofile
        
            #Set these variables - Unapproved X-Departmental task
            newTask.isxdepartmental = True
            newTask.taskstatus = 'U'
        
#TODO: UNCOMMENT WHEN THE LOGIN SYSTEM IS READY        
            #Set the origin & target departments.        
            #newTask.origindept = userprofile.dept
            #newTask.targetdept = userprofile.dept
        
            newTask.save()
        
            return HttpResponse ("Task Saved")
        else:
            return render_to_response ('tasks/task.html', {'form': form }, context_instance=RequestContext(request))
    else:
        form = CrossTaskForm (department)
        context = {'form': form}
        return render_to_response('tasks/task.html', context, context_instance=RequestContext(request))