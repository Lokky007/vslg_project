# -*- coding: utf-8 -*-
from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "Metoda_ve_main_wievs"}),
                            label='Jméno souboru')
    file = forms.FileField(label='Cesta')

    def clean(self):
        title = self.cleaned_data.get("title")
        file = self.cleaned_data.get("file")

        print title
        print file
