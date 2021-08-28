from django.forms import ModelForm
from django import forms
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('vote_total', 'vote_ratio', 'owner')
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add Title'}
        # )
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Description'}
        # )
