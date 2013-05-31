# ************** ERP - TASKS APP - VIEWS *********************
from tasks.models import Task
from tasks.forms import TaskForm

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404

from django.template import RequestContext


# _____________--- CORE CHECK FUNCTION ---______________#
def core_check (user):
    loginuser = user.get_profile()
    return loginuser.status == 2


# _____________--- TASK ADD VIEW ---______________#
#@login_required
#@user_passes_test (core_check)
def add_task(request):
    if request.method == 'POST':
        form= TaskForm(request.POST)
        newTask = form.save()
        return HttpResponseRedirect('/home')
    else:
        form=TaskForm()
        context = {'form': form}
        return render_to_response('tasks/task.htm', context, context_instance=RequestContext(request))
