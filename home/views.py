from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from home.forms import ChooseIdentityForm
from django.http import HttpResponseRedirect

def homepage ( request ):
    return render_to_response ( 'home/temp.html', locals(), context_instance = RequestContext(request) )

def choose_identity ( request ):
    
    if request.method == 'POST':
	print 'Post is happening :D'
	if identity_form.is_valid:
	    return HttpResponseRedirect ( '/home')
    identity_form = ChooseIdentityForm ( { 'coord_relations':request.user.erpuser.coord_relations, 'supercoord_relations':request.user.erpuser.supercoord_relations})
    return render_to_response ( 'home/choose_identity.html', locals(), context_instance = RequestContext(request) )

