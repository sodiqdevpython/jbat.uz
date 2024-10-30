from django import forms
from school.models import OverallClasses, OverallClasses, RoomsType, Rooms, RoomsEquipment

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

class OverallClassesForm(forms.ModelForm):
    class Meta:
        model = OverallClasses
        fields = ['name', 'rooms_amount']

class RoomsTypeForm(forms.ModelForm):
    class Meta:
        model = RoomsType
        fields = ['name']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['room_category', 'students_amount', 'room_class', 'room_number']


class RoomsEquipmentForm(forms.ModelForm):
    class Meta:
        model = RoomsEquipment
        fields = [
            'name', 'measure_type', 'amount', 'avilable_type', 'accepted_date', 
            'invert_number', 'entered_date', 'when_first_time_used', 'when_made',
            'image1', 'image2', 'image3', 'penny_by_year', 'xarakteri', 'equipment_type', 'room'
        ]
        widgets = {
            'accepted_date': forms.DateInput(attrs={'type': 'date'}),
            'entered_date': forms.DateInput(attrs={'type': 'date'}),
            'when_first_time_used': forms.DateInput(attrs={'type': 'date'}),
            'when_made': forms.NumberInput(attrs={'min': 1950, 'max': 2024}),
        }
