from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.views import View

from django.views.generic import CreateView, FormView

from complaints.forms import LoginForm, RegisterForm
from .models import Company

from django.contrib.auth import get_user_model
User = get_user_model()


class AdminUser(View):
    """User management across the application, admin access only"""
    def get(self, request):
        if not request.user.is_superuser:
            return render(request, 'admin/no_permissions.html')

        ctx = {
            'users': User.objects.all(),
            'link': "/adm"
        }
        return render(request, 'admin/user.html', ctx)


class AdminUserActivateView(View):
    """change active/inactive user, function only for admin"""
    def get(self, request, activate, user_id):
        if not request.user.is_superuser:
            return render(request, 'admin/no_permissions.html')

        user = User.objects.get(pk=user_id)
        user.is_active = activate
        user.save()
        return redirect('/adm/user/')