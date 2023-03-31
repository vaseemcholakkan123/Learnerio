from django import forms
from .models import *
from django.forms import ModelForm

class CourseForm(ModelForm):
    skills_offering = forms.ModelMultipleChoiceField(queryset=Skills.objects.all(),widget=forms.CheckboxSelectMultiple)
    category = forms.ModelChoiceField(queryset=Categories.objects.all(),widget=forms.Select)

    class Meta:
        model = Course
        fields = ('title','description','preview','duration','image','price','skills_offering','level','chapters','overview','category')
        widgets = {
            'description' : forms.Textarea(attrs={'rows':2}),
        }