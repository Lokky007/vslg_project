# -*- coding: utf-8 -*-
from django import forms



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "title"}),
                            label='Název souboru pro publikování na webu')
    file = forms.FileField(label='Cesta k souboru')
    status = forms.BooleanField(label="Po uložení ihned zveřejnit", initial=True)

    def clean(self):
        title = self.cleaned_data.get("title")
        file = self.cleaned_data.get("file")


class SearchForm(forms.Form):
    title = forms.CharField(max_length=50, label='', required=False,
                            widget=forms.TextInput(attrs={'class': "file_list_name file_list_name_search"}))

    author = forms.CharField(max_length=50, label='', required=False,
                             widget=forms.TextInput(attrs={'class': "file_list_uploadedBy file_list_uploadedBy_search"}))

class PasswordSetting(forms.Form):

    original_password = forms.CharField(label='Původní heslo', max_length=20, widget=forms.PasswordInput)
    new_password = forms.CharField(label='Nové heslo', max_length=20, widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(label='Opakujte nové heslo', max_length=20, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super(PasswordSetting, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        original_password = self.cleaned_data.get("original_password")
        new_password = self.cleaned_data.get("new_password")
        repeat_new_password = self.cleaned_data.get("repeat_new_password")

        if len(new_password) <= 5:
            raise forms.ValidationError("Heslo musí být delší 5 znaků")
        if new_password != repeat_new_password:
            raise forms.ValidationError("Hesla nejsou stejná")
        if not self.user.check_password(original_password):
            raise forms.ValidationError("Původní heslo nesouhlasí")

class UploadLinkForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "title"}),
                            label='Název odkazu pro publikování na webu')
    link = forms.CharField(label='Odkaz k publikaci')
    status = forms.BooleanField(label="Po uložení ihned zveřejnit", initial=True)

    def clean(self):
        title = self.cleaned_data.get("title")
        link = self.cleaned_data.get("link")

