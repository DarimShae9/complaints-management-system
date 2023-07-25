from django import forms
from django.core import validators

class LoginForm(forms.Form):
    login = forms.CharField(max_length=64, label='Login', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputEmail',
        'placeholder': 'inputLogin'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'inputPassword',
        'placeholder': 'inputPassword'
    }), label='Hasło')


class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=64, label='Login', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputFirstName',
        'placeholder': 'inputFirstName'
    }))
    lastname = forms.CharField(max_length=64, label='Login', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputFirstName',
        'placeholder': 'inputLastName'
    }))
    email = forms.CharField(max_length=64, label='Login', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputEmail',
        'placeholder': 'inputEmail'
    }), validators=Email)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'inputPassword',
        'placeholder': 'inputPassword'
    }), label='Hasło')
    passwordConf = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'inputPassword',
        'placeholder': 'inputPasswordConf'
    }), label='Hasło')
    companyName = forms.CharField(max_length=64, label='Login', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputFirstName',
        'placeholder': 'inputCompanyName'
    }))
    companyVat = forms.CharField(max_length=64, label='Login', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputEmail',
        'placeholder': 'inputCompanyVAT'
    }))