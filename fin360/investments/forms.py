from django import forms
from django.forms.widgets import ClearableFileInput

class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True

class PdfImportForm(forms.Form):
    arquivos = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True}),
        label='Arquivos PDF',
        help_text='Selecione até 15 arquivos PDF (máx. 15).',
    )

    def clean_arquivos(self):
        arquivos = self.files.getlist('arquivos')
        if not arquivos:
            raise forms.ValidationError('Envie ao menos um PDF.')
        if len(arquivos) > 15:
            raise forms.ValidationError('Máximo de 15 arquivos.')
        return arquivos
