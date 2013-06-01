from django import forms
from django.forms import ModelForm, Select
from tasks.models import Task
from users.models import ERPUser
from dept.models import Subdept


# _____________--- INTRADEPARTMENTAL TASK FORM ---______________#
class IntraTaskForm(ModelForm):
    #Temporary solution to provide options for selecting a taskforce.
    coords = forms.ModelMultipleChoiceField(queryset = ERPUser.objects.none())
    supercoords = forms.ModelMultipleChoiceField(queryset = ERPUser.objects.none())
    cores = forms.ModelMultipleChoiceField(queryset = ERPUser.objects.none())

    class Meta:
        model = Task
# TODO: Remove 'taskcreator', 'origindept', 'targetdept' fields. Put there only for testing until login system gets ready.
        fields = ['taskcreator', 'origindept', 'targetdept', 'deadline', 'subject', 'description',  'parenttask']
        
    #Framework for getting a QuerySet of Coords, Supercoords, and Cores.
    def __init__(self, department, *args, **kwargs):
        super (IntraTaskForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['coords'].queryset = ERPUser.objects.filter(coord_relations__dept=department)
        self.fields['supercoords'].queryset = department.supercoord_set.all()
        self.fields['cores'].queryset = department.core_set.all()
        


# _____________--- CROSSDEPARTMENTAL TASK FORM ---______________#
class CrossTaskForm(ModelForm):
    class Meta:
        model = Task
# TODO: Remove 'taskcreator', 'origindept', 'targetdept' fields. Put there only for testing until login system gets ready.
        fields = ['taskcreator', 'origindept', 'targetdept', 'deadline', 'subject', 'description', 'parenttask', 'targetsubdepts']
        
        
    def clean_targetsubdepts(self):
        value = self.cleaned_data['targetsubdepts']
        if len(value) > 1:
            raise forms.ValidationError("Select only one foreign subdepartment to assign the task to.")
        return value
    
    #Framework for getting a QuerySet of Subdepartments.
    def __init__(self, department, *args, **kwargs):
        super (CrossTaskForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['targetsubdepts'].queryset = Subdept.objects.exclude(dept=department)