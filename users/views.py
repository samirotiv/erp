# Create your views here.

from users.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, REDIRECT_FIELD_NAME
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404

def login(request):

    #Redirect logged in users
    if request.user.is_authenticated():
	return HttpResponseRedirect('/home/')

    if request.method == 'POST':

	#Authenticate the user
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        #if everything is in order
        if user is not None and user.is_active and not user.is_superuser:
            auth_login(request, user)

	    #Set things about the user. I am assuming that status, subdept etc are set a priori for users without multiple identities.
	    
	    #check for multiple identities
	    if user.erpuser.multiple_ids == True:  
		return HttpResponseRedirect('/home/choose_identity/')
	    
	    return HttpResponseRedirect('/home/')

	#If the username and password aren't in order
        invalid_login = True
        login_form = LoginForm()
        return render_to_response('users/login.html', locals(), context_instance=RequestContext(request))
    
    #rendering for the initial GET request
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
