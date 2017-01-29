from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
User = get_user_model()


class UserRegisterForm(forms.Form):
    user_login = forms.CharField(label='Nazev uctu', max_length=50)
    user_pass = forms.CharField(label='Heslo (min. 5 znaku)', max_length=20, widget=forms.PasswordInput)
    user_pass_check = forms.CharField(label='Opakujte heslo', max_length=20, widget=forms.PasswordInput)
    user_name = forms.CharField(label='Jmeno', max_length=50)
    user_last_name = forms.CharField(label='Prijmeni', max_length=50)
    user_email = forms.EmailField(label='Email', max_length=50)

    def clean(self):
        register_login = self.cleaned_data.get("user_login")
        register_pass = self.cleaned_data.get("user_pass")
        register_pass_check = self.cleaned_data.get("user_pass_check")
        register_name = self.cleaned_data.get("user_name")
        register_last_name = self.cleaned_data.get("user_last_name")
        register_email = self.cleaned_data.get("user_email")

        if User.objects.filter(username=register_login).exists():
            raise forms.ValidationError("Tento nayev uctu jiz registrovany je. Zadejte prosim")

        if (len(register_pass) <= 5):
            raise forms.ValidationError("Heslo musi byt delsi 5 znaku")

        if register_pass != register_pass_check:
            raise forms.ValidationError("Hesla nejsou stejna")


class UserLoginForm(forms.Form):
    login_name = forms.CharField(label='Ucet', max_length=50)
    login_pass = forms.CharField(label='Heslo', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        login_name = self.cleaned_data.get("login_name")
        login_pass = self.cleaned_data.get("login_pass")
        if login_name and login_pass:
            user = authenticate(username=login_name, password=login_pass)
            if user is None:
                raise forms.ValidationError("Nazev uctu neexistuje")
            if not user.check_password(login_pass):
                raise forms.ValidationError("Toto heslo je spatne")

            if not user.is_active:
                raise forms.ValidationError("Neni aktivni")

        return super(UserLoginForm, self).clean(*args, **kwargs)



