from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

class UserRegisterForm(forms.Form):
    user_login = forms.CharField(label='Nazev uctu', max_length=50)
    user_pass = forms.CharField(label='Heslo', max_length=20)
    user_pass_check = forms.CharField(label='Opakujte heslo', max_length=20)
    user_name = forms.CharField(label='Jmeno', max_length=50)
    user_last_name = forms.CharField(label='Prijmeni', max_length=50)
    user_email = forms.CharField(label='Email', max_length=50)

user = get_user_model()

class UserLoginForm(forms.Form):
    login_name = forms.CharField(label='Ucet', max_length=50)
    login_pass = forms.CharField(label='Heslo', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        login_name = self.cleaned_data.get("login_name")
        login_pass = self.cleaned_data.get("login_pass")
        if login_name and login_pass:
            user = authenticate(username=login_name, password=login_pass)
            print user
            if user is None:
                raise forms.ValidationError("Nazev uctu neexistuje")
            if not user.check_password(login_pass):
                raise forms.ValidationError("Toto heslo je spatne")

            if not user.is_active:
                raise forms.ValidationError("Neni aktivni")

        return super(UserLoginForm, self).clean(*args, **kwargs)



