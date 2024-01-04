from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'importance']
        widgets = {
            'title': forms.TextInput(attrs={'autocomplete': 'off', 'autofocus': 'true'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off'}),
        }