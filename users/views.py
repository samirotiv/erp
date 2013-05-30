# Create your views here.

from users.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, REDIRECT_FIELD_NAME
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response

def login(request):

    if request.user.is_authenticated():
	return HttpResponseRedirect('/home/')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active and not user.is_superuser:
            auth_login(request, user)
	    return HttpResponseRedirect('/home/')
        invalid_login = True
        login_form = LoginForm()
        return render_to_response('users/login.html', locals(), context_instance=RequestContext(request))
    else:
	login_form = LoginForm()
        return render_to_response('users/login.html', locals(), context_instance=RequestContext(request))
 
