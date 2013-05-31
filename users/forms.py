from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(help_text='Your ERP username')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password.')

