
from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from saudi_id_validator import validate
from .models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    dateOfBirth = forms.DateField(label='Your date of birth', widget=forms.DateInput(attrs={'type': 'date'}))
    phone = PhoneNumberField()
    nationalId = forms.IntegerField(label='Your ID number')


    class Meta:
        model = User
        fields = ['name', 'nationalId', 'email', 'phone', 'dateOfBirth',  'password1', 'password2']

    def clean_nationalId(self):
        nationalId_passed = self.cleaned_data.get("nationalId")
        is_valid = validate(nationalId_passed)  # could also be an integer
        if is_valid == False:
            raise forms.ValidationError("Not valid ID number")
        return nationalId_passed

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.name = self.cleaned_data["name"]
        user.phone = self.cleaned_data["phone"]
        user.dateOfBirth = self.cleaned_data["dateOfBirth"]
        user.nationalId = self.cleaned_data["nationalId"]

        if commit:
            user.save()
        return user
