from django import forms
from django.contrib.auth.forms import UserCreationForm

class ExtUserCreationForm(UserCreationForm):
    """
    Extended user creation form.
    """
    email = forms.EmailField(max_length=75)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
                user.save()
        return user
