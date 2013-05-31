# Create your views here.

from users.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, REDIRECT_FIELD_NAME
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404

def login(request):

    if request.user.is_authenticated():
	return HttpResponseRedirect('/home/') #Redirect if logged in.
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active and not user.is_superuser:
            auth_login(request, user)#if login forms is valid
	    if user.erpuser.multiple_ids == True:   #check multiple identities
		return HttpResponseRedirect('/home/choose_identity/')
	    return HttpResponseRedirect('/home/')
        invalid_login = True
        login_form = LoginForm()
        return render_to_response('users/login.html', locals(), context_instance=RequestContext(request))
    else:
	login_form = LoginForm()
        return render_to_response('users/login.html', locals(), context_instance=RequestContext(request))
 
def logout(request):
    """
        View for logging out users from the session.
    """
    if request.user.is_authenticated():
        auth_logout(request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')
