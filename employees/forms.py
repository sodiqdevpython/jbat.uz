from django import forms
from school.models import OverallClasses

class OverallClassesForm(forms.ModelForm):
    class Meta:
        model = OverallClasses
        fields = ['organization', 'name', 'rooms_amount']
        
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sinf nomi'}),
            'rooms_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Xonalar soni'}),
        }
        
        labels = {
            'organization': 'Tashkilot',
            'name': 'Sinf nomi',
            'rooms_amount': 'Xonalar soni',
        }
