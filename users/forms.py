from django import forms
from users.models import ERPUser
from dept.models import Dept, Subdept

class LoginForm(forms.Form):

    username=forms.CharField(help_text='Your ERP username')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password.')


class ChooseIdentityForm(forms.Form):

    coordships = forms.ModelChoiceField( queryset = Subdept.objects.none(), required=False, help_text = 'Choose a coordship' )
    supercoordships = forms.ModelChoiceField( queryset = Dept.objects.none(), required=False, help_text = 'Choose a supercoordship' )

    #Framework for getting a QuerySet of Coordships and Supercoordships
    def __init__(self, curruser, *args, **kwargs):
        super (ChooseIdentityForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['coordships'].queryset = curruser.coord_relations.all() 
        self.fields['supercoordships'].queryset = curruser.supercoord_relations.all()
 
