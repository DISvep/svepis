from django import forms
from .models import PostComment, VideoComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add your comment...',
                'rows': 1,
                'style': 'border: none; resize: none;',
                'id': 'commentAdd'
            })
        }
        

class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add your comment...',
                'rows': 1,
                'style': 'border: none; resize: none;',
                'id': 'commentAdd'
            })
        }
    