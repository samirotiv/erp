

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
def dash_view(request, section="default"):
    userprofile = request.user.get_profile()
    
    #Default Ordering
    order_by = request.GET.get('order_by', 'deadline')
    
    # Initialize a blank Query dictionary.
    query_dictionary = {}
    
    #Assigning one of the above values
    if section == "dept_tasks":
        query_dictionary["tasks"] = userprofile.dept.todo_task_set.order_by(order_by)
        
    elif section == "subdept_tasks":
        query_dictionary["tasks"] = userprofile.subdept.task_set.order_by(order_by)
        
    elif section == "dept_created_crosstasks":
        query_dictionary["tasks"] = userprofile.dept.created_task_set.filter(isxdepartmental=True).order_by(order_by)
        
    elif section == "approval_pending_tasks":
        query_dictionary["tasks"] = userprofile.dept.created_task_set.filter(taskstatus='U').order_by(order_by)
        
    elif section == "dept_cross_tasks":
        query_dictionary["tasks"] = userprofile.dept.todo_task_set.filter(isxdepartmental=True).order_by(order_by) #Remove if necessary.
        
    else section == "usertasks":        #Made User Tasks the default section
        query_dictionary["tasks"] = userprofile.task_set.order_by(order_by)
    
    query_dictionary["section"] = section
    
    
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
        
        