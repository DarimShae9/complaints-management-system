from django import forms
from .models import Company
from django.contrib.auth import get_user_model
User = get_user_model()


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
    email = forms.EmailField(max_length=64, label='Login', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputEmail',
        'placeholder': 'inputEmail'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'inputPassword',
        'placeholder': 'inputPassword'
    }))
    passwordConf = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'inputPassword',
        'placeholder': 'inputPasswordConf'
    }))
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

    def clean(self):
        """
        Validation of basic data such as the
        company's unique VAT number,
        unique e-mail address,
        correctness of passwords...
        :return:
        """
        super().clean()
        error = {}

        if len(self.cleaned_data['password']) < 8:
            error.update({'password': "password must be longer than 8 characters!"})
        if self.cleaned_data['password'] != self.cleaned_data['passwordConf']:
            error.update({'password': "The passwords are not the same!"})

        if len(User.objects.filter(email=self.cleaned_data['email'])) != 0:
            error.update({'email': 'This email address is already taken!'})

        if len(self.cleaned_data['companyVat']) != 9:
            error.update({'companyVat': 'The vat number must only have 9 numbers!'})
        if self.cleaned_data['companyVat'].isnumeric() != True:
            error.update({'companyVat': 'The VAT number should consist of numbers only!'})
        if len(Company.objects.filter(nip=self.cleaned_data['companyVat'])) != 0:
            error.update({'companyVat': 'Company already exists!'})

        raise forms.ValidationError(error)
