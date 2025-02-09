
from .models import Customer
from django import forms


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

