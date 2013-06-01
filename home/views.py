from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from home.forms import ChooseIdentityForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def homepage ( request ):
    return render_to_response ( 'home/temp.html', locals(), context_instance = RequestContext(request) )

@login_required
def choose_identity ( request ):
    
    #This is a Boolean which informs the template that the user has made no error
    noerror = True

    if request.method == 'POST':
	identity_form = ChooseIdentityForm (request.user.erpuser, request.POST)

	if identity_form.is_valid():
	    cd = identity_form.cleaned_data

	    #if they don't choose anything
	    if cd['coordships'] == None and cd['supercoordships'] == None:
		print 'a'
		noerror = False
		return render_to_response ( 'home/choose_identity.html', locals(), context_instance = RequestContext(request) )

	    #if they make choices in both.
	    if not cd['coordships'] == None and not cd['supercoordships'] == None:
		print 'b'
		noerror = False
		return render_to_response ( 'home/choose_identity.html', locals(), context_instance = RequestContext(request) )
	    
	    #if everything is in order, we can now set the identity and let him/her be on his way. :)
	    userprofile = request.user.erpuser

	    #if he's chosen a coordship
	    if not cd['coordships'] == None:
		print 'c'
		userprofile.status = 0
		userprofile.subdept = cd['coordships'] #which coordship he's chosen. Don't know if this is necessary, but it can't hurt
		
	    #if he's chosen a supercoordship
	    else:
		userprofile.status = 1 #supercoord
	    userprofile.save()
	    return HttpResponseRedirect ('/home/')
    identity_form = ChooseIdentityForm ( curruser = request.user.erpuser )
    return render_to_response ( 'home/choose_identity.html', locals(), context_instance = RequestContext(request) )

