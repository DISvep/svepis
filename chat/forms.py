from django import forms
from .models import GroupChat


class GroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = {'name', 'avatar'}
        labels = {'name': '', 'avatar': ''}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Name your group...",
            })
        }

    def __init__(self, *args, **kwargs):
        super(GroupChatForm, self).__init__(*args, **kwargs)

        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})


class EditGroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = {'name', 'avatar'}
        labels = {'name': '', 'avatar': ''}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Name your group...",
                'id': 'editGroupName',
            })
        }

    def __init__(self, *args, **kwargs):
        super(EditGroupChatForm, self).__init__(*args, **kwargs)

        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'id': 'editGroupAvatar'})
