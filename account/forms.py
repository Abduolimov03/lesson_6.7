from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Parol', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Parolni tasdiqlang', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2 or password1 != password2:
            raise forms.ValidationError('Parollar bir xil emas')

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=120, label='Login')
    password = forms.CharField(label='Parol', widget=forms.PasswordInput)


class ChangePassForm(forms.Form):
    old_pass = forms.CharField(label='eski parol', widget=forms.PasswordInput)
    new_pass = forms.CharField(label='yangi parol', widget=forms.PasswordInput)
    confirm_pass = forms.CharField(label='parolni tsdiqlang', widget=forms.PasswordInput)
    code = forms.CharField(label='Email ga yuborilgan kod', max_length=6)

    def clean(self):
        cleane_data = super().clean()
        new_pass = self.cleaned_data['new_pass']
        confirm_pass = self.cleaned_data['confirm_pass']
        if new_pass != confirm_pass:
            raise forms.ValidationError('Parollar mos emas')

        return cleane_data

