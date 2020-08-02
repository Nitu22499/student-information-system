from django import forms
from Assignmnet.models import Assignment
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('__all__')
        exclude = ('subject', )

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_teacher = True
    #     if commit:
    #         user.save()

    #     teacher = .objects.create(user=user)
    #     return user