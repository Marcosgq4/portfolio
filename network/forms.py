from django import forms
from .models import New_Post

class NewPostForm(forms.ModelForm):
    class Meta:
        model = New_Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': "What's on your mind?"}),
        }
    
    
