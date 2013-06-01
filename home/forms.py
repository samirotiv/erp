from django import forms
from dept.models import Dept, Subdept

class ChooseIdentityForm(forms.Form):
    coordships = forms.ModelChoiceField( queryset = Subdept.objects.all(), required=False, help_text = 'Choose a coordship' )
    supercoordships = forms.ModelChoiceField( queryset = Dept.objects.all(), required=False, help_text = 'Choose a supercoordship' )
