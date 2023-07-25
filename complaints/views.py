from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render
from django.views import View

from django.views.generic import CreateView, FormView

from complaints.forms import LoginForm, RegisterForm


# Create your views here.


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
        ctx = {
            'form': form,
            'message': 'Przesłano POST !'
        }
        return render(request, 'register.html', ctx)