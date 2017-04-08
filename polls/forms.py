# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
User = get_user_model()


class UserRegisterForm(forms.Form):
    user_login = forms.CharField(label='Název úctu (min. 5 znaku)', max_length=50)
    user_pass = forms.CharField(label='Heslo (min. 5 znaku)', max_length=20, widget=forms.PasswordInput)
    user_pass_check = forms.CharField(label='Opakujte heslo', max_length=20, widget=forms.PasswordInput)
    user_name = forms.CharField(label='Jméno', max_length=50)
    user_last_name = forms.CharField(label='Přijmení', max_length=50)
    user_email = forms.EmailField(label='Email', max_length=50)

    def clean(self):
        register_login = self.cleaned_data.get("user_login")
        register_pass = self.cleaned_data.get("user_pass")
        register_pass_check = self.cleaned_data.get("user_pass_check")
        register_name = self.cleaned_data.get("user_name")
        register_last_name = self.cleaned_data.get("user_last_name")
        register_email = self.cleaned_data.get("user_email")

        if User.objects.filter(username=register_login).exists():
            raise forms.ValidationError("Tento název účtu již registrovaný je. Zadejte prosím jiný")

        if (len(register_login) <= 5):
            raise forms.ValidationError("Název účtu musí být delší 5 znaků")

        if (len(register_pass) <= 5):
            raise forms.ValidationError("Heslo musí být delší 5 znaků")

        if register_pass != register_pass_check:
            raise forms.ValidationError("Hesla nejsou stejná")


class UserLoginForm(forms.Form):
    login_name = forms.CharField(label='Účet', max_length=50)
    login_pass = forms.CharField(label='Heslo', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        login_name = self.cleaned_data.get("login_name")
        login_pass = self.cleaned_data.get("login_pass")
        if login_name and login_pass:
            user = authenticate(username=login_name, password=login_pass)
            if user is None or not user.check_password(login_pass):
                raise forms.ValidationError("Heslo nebo název účtu je nesprávné")

            if not user.is_active:
                raise forms.ValidationError("Uživatel není aktivní")

        return super(UserLoginForm, self).clean(*args, **kwargs)



