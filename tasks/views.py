# ************** ERP - TASKS APP - VIEWS *********************
from tasks import Task


def core_check (user):
    loginuser = user.get_profile()
    return loginuser.status == 2


# _____________--- TASK ADD VIEW ---______________#
@login_required
@user_passes_test (core_check)
def AddTask(request):
    if request.method == 'POST':
        form= TaskForm(request.POST)
        newTask = form.save()
        return HttpResponseRedirect('/home')
    else:
        form=TaskForm()
        context = {'form': form}
        return render_to_response('tasks/task.htm', context, context_instance=RequestContext(request))