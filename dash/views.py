

# ************** ERP - DASH APP - VIEWS ********************* #


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


from tasks.models import Task



# _____________--- DASH VIEW ---______________#
"""
QUERIES TO RETRIEVE:
1.  The user’s tasks.
2.  Tasks assigned to the department
3.  Tasks assigned to the subdepartment
4.  The Crosstasks created by the department
5.  Tasks pending approval
6.  ?Crosstasks _to_ the department?


"""
@login_required
def dash_view(request):
    userprofile = request.user.get_profile()

    # Initialize a blank Query dictionary.
    query_dictionary = {}
    
    #Assigning the above values
    query_dictionary["user_tasks"] = userprofile.task_set.all()
    query_dictionary["dept_tasks"] = userprofile.dept.todo_task_set.all()
    query_dictionary["subdept_tasks"] = userprofile.subdept.task_set.all()
    query_dictionary["dept_created_crosstasks"] = userprofile.dept.created_task_set.filter(isxdepartmental=True)
    query_dictionary["approval_pending_tasks"] = userprofile.dept.created_task_set.filter(taskstatus='U')
    query_dictionary["dept_tasks"] = userprofile.dept.todo_task_set.filter(isxdepartmental=True) #Remove if necessary.
    
    
    #RENDERING THE TEMPLATE
    # For a Coordinator
    if userprofile.status == 0:
        return render_to_response ('dash/coord.html', query_dictionary, context_instance=RequestContext(request))
        
    # For a Supercoordinator
    if userprofile.status == 1:
        return render_to_response ('dash/supercoord.html', query_dictionary, context_instance=RequestContext(request))
        
    # For a Core
    if userprofile.status == 2:
        return render_to_response ('dash/core.html', query_dictionary, context_instance=RequestContext(request))
        
        