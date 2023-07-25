from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.views import View

from django.views.generic import CreateView, FormView

from complaints.forms import LoginForm, RegisterForm
from .models import Company

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class HomeView(View):
    def get(self, request):
        return redirect('/login/')


class LoginView(View):
    def get(self, request):
        ctx = {
            'form': LoginForm(),
            'message': 'Wpisz dane aby się zalogować',
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {
            'form': form,
            'message': 'POST - method',
        }
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                ctx.update({'message': 'udało się zalogować'})
            else:
                ctx.update({'message': "Niepoprawny login lub hasło"})
        return render(request, 'login.html', ctx)


class RegisterView(View):
    def get(self, request):
        ctx = {
            'form': RegisterForm()
        }
        return render(request, 'register.html', ctx)


    def post(self, request):
        form = RegisterForm(request.POST)
        ctx = {}

        if form.is_valid():
            company = Company.objects.create(
                name=form.cleaned_data['companyName'],
                nip=form.cleaned_data['companyVat']
            )
            user_atr = {
                'first_name': form.cleaned_data['firstname'],
                'last_name': form.cleaned_data['lastname'],
                'company': company,
                'is_active': 0,
                'user_custom_role': 2
            }
            user = User.objects.create_user(
                form.cleaned_data['login'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                **user_atr
            )
            ctx.update({'message': 'Account added, wait for administrator activation.'})
        else:
            ctx.update({
                'message': 'The form contains errors, please correct them',
                'form': form
            })
        return render(request, 'register.html', ctx)
