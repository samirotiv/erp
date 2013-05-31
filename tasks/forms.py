from django import forms
from django.forms import ModelForm, Select
from tasks.models import Task

# _____________--- INTRADEPARTMENTAL TASK FORM ---______________#
class IntraTaskForm(ModelForm):
    class Meta:
        model = Task
# TODO: Remove 'taskcreator', 'origindept', 'targetdept' fields. Put there only for testing until login system gets ready.
        fields = ['taskcreator', 'origindept', 'targetdept', 'deadline', 'subject', 'description', 'taskforce', 'parenttask']
        
        


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