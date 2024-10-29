from django import forms
from .models import Organizations, Regions, Districts, Cities, UserProfile
from django.forms import NumberInput


class RegionForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = ['name']

class DistrictForm(forms.ModelForm):
    class Meta:
        model = Districts
        fields = ['region', 'name']

class CityForm(forms.ModelForm):
    class Meta:
        model = Cities
        fields = ['region', 'name']


class UpdateOrganizationForm(forms.ModelForm):

    class Meta:
        model = Organizations
        fields = [
            'organization_number',
            'name',
            'education_type',
            'power',
            'vr_mode_url',
            'is_inclusive',
            'district',
            'city',
            'region',
            'latitude',
            'longitude',
            'students_amount'
        ]

        widgets = {
            'organization_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Muassasa raqami', 'maxlength': 4}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Muassasa nomi'}),
            'education_type': forms.Select(attrs={'class': 'form-control'}),
            'power': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quvvat'}),
            'vr_mode_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_inclusive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'students_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kenglik'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uzunlik'})
        }

        labels = {
        'organization_number': 'Muassasa raqami',
        'name': 'Muassasa nomi',
        'education_type': 'Ta’lim turi',
        'power': 'Quvvat',
        'vr_mode_url': "Muassasa web sahifasi",
        'is_inclusive': 'Inkluziv muassasa',
        'district': 'Tuman',
        'city': 'Shahar',
        'region': 'Viloyat',
        'students_amount': "O'quvchilar sig'imi",
        'latitude': 'Kenglik',
        'longitude': 'Uzunlik'
    }


class CreateOrganizationForm(forms.ModelForm):

    admin = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(is_selected=False, is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
        )

    class Meta:
        model = Organizations
        fields = [
            'organization_number',
            'name',
            'education_type',
            'power',
            'vr_mode_url',
            'is_inclusive',
            'district',
            'city',
            'region',
            'latitude',
            'longitude',
            'admin',
            'students_amount'
        ]

        widgets = {
            'organization_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Muassasa raqami'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Muassasa nomi'}),
            'education_type': forms.Select(attrs={'class': 'form-control'}),
            'power': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quvvat'}),
            'vr_mode_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_inclusive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kenglik'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uzunlik'}),
            'admin': forms.TextInput(attrs={'class': 'form-control'}),
            'students_amount': forms.TextInput(attrs={'class': 'form-control'})
        }

        labels = {
        'organization_number': 'Muassasa raqami',
        'name': 'Muassasa nomi',
        'education_type': 'Ta’lim turi',
        'power': 'Quvvat',
        'vr_mode_url': "Muassasa web sahifasi",
        'is_inclusive': 'Inkluziv muassasa',
        'district': 'Tuman',
        'city': 'Shahar',
        'region': 'Viloyat',
        'latitude': 'Kenglik',
        'longitude': 'Uzunlik',
        'admin': 'Admin',
        'students_amount': "O'quvchilar sig'imi",
    }