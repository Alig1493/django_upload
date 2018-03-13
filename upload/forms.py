from django import forms

from upload.models import File


class FileForm(forms.ModelForm):
    """Upload files with this form"""

    file_field = forms.FileField(widget=forms.ClearableFileInput(
        attrs={
            'multiple': True,
            'type': 'file',
            'name': 'file',
            'accept': '.xls, .xlsx, .csv',
            'class': 'custom-file-input',
            'id': 'file-picker'
        }
    ))

    class Meta:
        model = File
        fields = '__all__'
