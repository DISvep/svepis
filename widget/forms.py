from django import forms
from .models import Widget


class WidgetForm(forms.ModelForm):
    class Meta:
        model = Widget
        fields = ['widget_type', 'content', 'image', 'x_position', 'y_position']
        