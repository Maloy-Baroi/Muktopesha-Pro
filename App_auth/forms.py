from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from App_auth.models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class SkillListModelForm(forms.ModelForm):
    class Meta:
        model = SkillListModel
        exclude = ['user']


class EducationModelForm(forms.ModelForm):
    starting_year = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    passing_year = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'required': 'false'}))

    class Meta:
        model = EducationModel
        exclude = ['user', 'active']


class Extra_curricular_Activities_ModelForm(forms.ModelForm):
    perform_time = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Extra_curricular_Activities_Model
        exclude = ['user']


class Co_curricular_Activities_ModelForm(forms.ModelForm):
    perform_time = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Co_curricular_Activities_Model
        exclude = ['user']


class ExperiencesModelForm(forms.ModelForm):
    starting_year = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    leaving_year = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = ExperiencesModel
        exclude = ['user']


class FreelancerProfileModelForm(forms.ModelForm):
    Date_of_Birth = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile(ex: +8801'}))

    Bkash_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile(ex: +8801'}))

    class Meta:
        model = FreelancerProfileModel
        exclude = ['user', 'activity_status', 'stars']


class BuyerProfileModelForm(forms.ModelForm):
    Date_of_Birth = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address (House, City, State-zipcode)'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}))
    
    class Meta:
        model = BuyerProfileModel
        fields = [
            'profile_picture',
            'full_name',
            'phone_number',
            'address',
            'description',
            'Date_of_Birth',
            'gender'
        ]

    def __init__(self, *args, **kwargs):
        super(BuyerProfileModelForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = "Write Your Bio."



class LanguagesModelForm(forms.ModelForm):
    class Meta:
        model = LanguagesModel
        exclude = ['user']



class SkillListModelForm(forms.ModelForm):
    class Meta:
        model = SkillListModel
        exclude = ['user']
