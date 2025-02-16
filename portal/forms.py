from django import forms
from .models import Portal


class PortalForm(forms.ModelForm):
    class Meta:
        model = Portal
        fields = ['avatar', 'banner', 'about']
        widgets = {
            'about': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super(PortalForm, self).__init__(*args, **kwargs)
        
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
        self.fields['banner'].widget.attrs.update({'class': 'form-control'})
    