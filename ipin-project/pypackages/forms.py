from django import forms
from .models import Wheel

class WheelUploadForm(forms.ModelForm):
    class Meta:
        model = Wheel
        fields = ['file_path']
        widgets = {
            'file_path': forms.ClearableFileInput(attrs={'accept': '.whl'}),
        }
