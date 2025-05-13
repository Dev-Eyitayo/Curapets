# admin_forms.py
from django import forms
from .models import DoctorProfile
import json
from django_json_widget.widgets import JSONEditorWidget


class DoctorProfileAdminForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        widgets = {
            'available_days': forms.CheckboxSelectMultiple,
            'available_times': forms.Textarea(attrs={'rows': 5, 'cols': 60})
        }

    def clean_available_times(self):
        value = self.cleaned_data.get('available_times', {})
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid JSON format.")
        return value



class DoctorProfileAdminForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        widgets = {
            'available_days': forms.CheckboxSelectMultiple,
            'available_times': JSONEditorWidget(),
        }
