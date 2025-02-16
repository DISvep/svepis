from django import forms
from .models import Widget


class WidgetForm(forms.ModelForm):
    class Meta:
        model = Widget
        fields = ['widget_type', 'content', 'image']
        labels = {'content': '', 'image': ''}
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type something...',
                'style': 'border: none; resize: none; display: none;',
                'id': 'content',
                'rows': 1
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)
        
        self.fields['widget_type'].widget.attrs.update({'class': 'form-control', 'id': 'widgetType'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'style': 'display: none', 'id': 'image'})
        