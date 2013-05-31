from django import forms
from dept.models import Dept, Subdept

class ChooseIdentityForm(forms.Form):
    coordships = forms.ModelMultipleChoiceField( queryset = Subdept.objects.all(), help_text = 'Choose a coordship' )
    supercoordships = forms.ModelMultipleChoiceField( queryset = Dept.objects.all(), help_text = 'Choose a supercoordship' )
