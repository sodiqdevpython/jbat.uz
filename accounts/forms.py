from django import forms
from school.models import UserProfile


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name',
            'born_in', 'father_name', 'passport_id',
            'manzil', 'pinfl', 'position', 'tel_number',
            'command_expire','command_pdf'
        )

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name',
            'born_in', 'father_name', 'passport_id',
            'manzil', 'pinfl', 'position', 'tel_number',
            'command_expire','command_pdf'
        )