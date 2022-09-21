from django import forms
from App_main.models import *


class OfferedToDoTheJobModelForm(forms.ModelForm):
    class Meta:
        model = OfferedToDoTheJobModel
        fields = ['offer_text']


class JobCategoriesModelForm(forms.ModelForm):
    class Meta:
        model = JobCategoriesModel
        fields = "__all__"


class SubCategoriesModelForm(forms.ModelForm):
    class Meta:
        model = SubCategoriesModel
        fields = "__all__"


class JobModelForm(forms.ModelForm):
    validate_until = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = JobModel 
        exclude = ['author', 'status']


class ProductSubmissionModelForm(forms.ModelForm):
    class Meta:
        model = ProductSubmissionModel
        exclude = ['sender', 'receiver', 'job']


