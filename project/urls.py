"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from complaints.views import LoginView, RegisterView, HomeView, LogoutView, PanelHomeView, UserAddView, UserManagementView, \
    UserManagementActivateView
from complaints.views_admin import AdminUser, AdminUserActivateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adm/user/', AdminUser.as_view()),
    path('adm/<int:activate>/<int:user_id>/', AdminUserActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('', HomeView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('panel/home/', PanelHomeView.as_view()),
    path('panel/add_user/', UserAddView.as_view()),
    path('panel/users/', UserManagementView.as_view()),
    path('panel/users/<int:activate>/<int:user_id>/', UserManagementActivateView.as_view()),
]
