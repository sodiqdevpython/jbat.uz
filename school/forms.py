from django import forms
from .models import Organizations, Regions, Districts, Cities

class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organizations
        fields = ('organization_number', 'name', 'education_type', 'power', 'vr_mode_url', 'is_inclusive', 'rating', 'district', 'city', 'is_city', 'region', 'ball', 'latitude', 'longitude', )

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

class CreateOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organizations
        fields = ('organization_number', 'name', 'education_type', 'power', 'vr_mode_url', 'is_inclusive', 'district', 'city', 'region', 'ball', 'latitude', 'longitude', 'admin', )