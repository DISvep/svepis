from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'description', 'preview', 'video']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Video name...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Video description...',
                'style': 'border: none; resize: none;',
                'id': 'videoArea',
                'rows': 1,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        
        self.fields['preview'].widget.attrs.update({'class': 'form-control', 'accept': 'image/*'})
        self.fields['video'].widget.attrs.update({'class': 'form-control', 'accept': '.mp4'})
