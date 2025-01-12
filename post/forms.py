from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'content'}
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write down your thoughts...',
                'style': 'border: none; resize: none;',
                'id': 'postArea',
                'rows': 1,
            })
        }
    