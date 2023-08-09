from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.views import View

from django.views.generic import CreateView, FormView

from complaints.forms import LoginForm, RegisterForm, AddCompanyUserForm, NewCompaintForm, \
    MessageForm, ProductForm, StatusForm
from .models import Company, Order, Product, Message, STATUS_LIST
from .function import update_modification_time, historic_entry

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class HomeView(View):
    def get(self, request):
        return redirect('/login/')


class LoginView(View):
    """
    login page view
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/panel/home/')
        ctx = {
            'form': LoginForm(),
            'message': 'Wpisz dane aby się zalogować',
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                ctx.update({'message': "Zalogowany"})
                return redirect('/panel/home/', kwargs={ 'message': 'zalogowany' })
            else:
                ctx.update({'message': "Niepoprawny login lub hasło"})
        return render(request, 'login.html', ctx)


class RegisterView(View):
    """login page view"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/panel/home/')

        ctx = {
            'form': RegisterForm()
        }
        return render(request, 'register.html', ctx)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/panel/home/')

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


class LogoutView(View):
    """logout view"""
    def get(self, request):
        logout(request)
        return redirect('/login/')


class PanelHomeView(View):
    """start page for logged in users, changelog by default"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        return render(request, 'user/home.html')


class UserAddView(View):
    """
    View only for the business owner.
    Ability to create accounts for your own employees.
    """
    def get(self, request):
        if request.user.user_custom_role != 2:
            return render(request, 'admin/no_permissions.html', {'message': 'Do you want to create a user of your company? Ask your boss for access.'})
        ctx = {
            'form': AddCompanyUserForm()
        }
        return render(request, 'user/user_add.html', ctx)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if request.user.user_custom_role != 2:
            return render(request, 'admin/no_permissions.html')
        form = AddCompanyUserForm(request.POST)

        if form.is_valid():
            ctx = {
                'message': "New user created!"
            }

            more_data = {
                'user_custom_role': 3,
                'company_id': request.user.company_id,
                'first_name': form.cleaned_data['firstname'],
                'last_name': form.cleaned_data['lastname'],
            }
            User.objects.create_user(
                username=form.cleaned_data['login'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                **more_data
            )
            return render(request, 'admin/no_permissions.html', ctx)
        else:
            ctx = {
                'form': form
            }
            return render(request, 'user/user_add.html', ctx)

class UserManagementView(View):
    """
    view only for the owner of the company
    user can be activated and deactivated
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if request.user.user_custom_role != 2:
            return render(request, 'admin/no_permissions.html',
                          {'message': 'Want to manage users? Ask your boss for access.'})

        ctx = {
            'users': User.objects.filter(company_id=request.user.company_id),
            'link': '/panel/users'
        }
        return render(request, 'admin/user.html', ctx)


class UserManagementActivateView(View):
    """user activation and deactivation view"""
    def get(self, request, activate, user_id):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if request.user.user_custom_role != 2:
            return render(request, 'admin/no_permissions.html',
                          {'message': 'Want to manage users? Ask your boss for access.'})
        user = User.objects.get(pk=user_id)
        if user.user_custom_role == 2:
            return render(request, 'admin/no_permissions.html', {'message': "You can't deactivate the business owner ;)"})


        if user.company_id != request.user.company_id:
            return render(request, 'admin/no_permissions.html',
                          {'message': 'This is not your employee!!'})
        user.is_active = activate
        user.save()
        return redirect('/panel/users/')


class ComplaintListView(View):
    """list of all complaints"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        ctx = {
            'orders': Order.objects.filter(company=request.user.company_id).order_by('-modification_date'),
            'status_list': STATUS_LIST
        }
        return render(request, 'user/complaints_list.html', ctx)


class AddCompaintView(View):
    """view of adding a new complaint"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        ctx = {
            'form': NewCompaintForm()
        }
        return render(request, 'user/add_complaint.html', ctx)


    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        form = NewCompaintForm(request.POST)
        if form.is_valid():
            more_data = {
                'company_id': request.user.company_id,
            }
            order = Order.objects.create(
                number=form.cleaned_data['number'],
                **more_data
            )
            return redirect(f'/panel/show-complaint/{order.id}/')

        ctx = {
            'form': form
        }
        return redirect('/panel/add-complaint/', ctx)


class ShowComplaintView(View):
    """view of a single complaint"""
    def get(self, request, complaint_id):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if len(Order.objects.filter(pk=complaint_id)) != 1:
            return render(request, 'admin/no_permissions.html', {'message': 'There is no such order'})
        order = Order.objects.get(pk=complaint_id)
        if request.user.company_id != order.company_id:
            return render(request, 'admin/no_permissions.html', {'message': 'This is not your order!'})

        ctx = {
            'order': order,
            'products': Product.objects.filter(order=order),
            'messages': Message.objects.filter(order=order),
            'message_form': MessageForm(),
            'product_form': ProductForm(),
            'status_form': StatusForm(initial={'status': order.status}),
        }
        return render(request, 'user/show_complaint.html', ctx)


class AddMessageView(View):
    """view adding a message"""
    def post(self, request, order_id):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if len(Order.objects.filter(pk=order_id)) != 1:
            return render(request, 'admin/no_permissions.html', {'message': 'There is no such order'})
        order = Order.objects.get(pk=order_id)
        if request.user.company_id != order.company_id:
            return render(request, 'admin/no_permissions.html', {'message': 'This is not your order!'})

        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                user=request.user,
                order=order,
                text=form.cleaned_data['text']
            )
            update_modification_time(order.id)
            return redirect(f'/panel/show-complaint/{order_id}/')
        ctx = {
            'order': order,
            'products': Product.objects.filter(order=order),
            'messages': Message.objects.filter(order=order),
            'message_form': MessageForm(),
            'product_form': ProductForm(),
        }
        return render(request, 'user/show_complaint.html', ctx)


class AddProductView(View):
    """view adding a message"""
    def post(self, request, order_id):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if len(Order.objects.filter(pk=order_id)) != 1:
            return render(request, 'admin/no_permissions.html', {'message': 'There is no such order'})
        order = Order.objects.get(pk=order_id)
        if request.user.company_id != order.company_id:
            return render(request, 'admin/no_permissions.html', {'message': 'This is not your order!'})

        form = ProductForm(request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price']
            )
            order = Order.objects.get(pk=order_id)
            order.product.add(product)
            order.save()

            update_modification_time(order.id)
            historic_entry(order_id, request.user, f"User add product: {product.name}")
            return redirect(f'/panel/show-complaint/{order_id}/')
        ctx = {
            'order': order,
            'products': Product.objects.filter(order=order),
            'messages': Message.objects.filter(order=order),
            'message_form': MessageForm(),
            'product_form': ProductForm(),
        }
        return render(request, 'user/show_complaint.html', ctx)


class ChangeStatusView(View):
    """status changing view"""
    def post(self, request, order_id):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if len(Order.objects.filter(pk=order_id)) != 1:
            return render(request, 'admin/no_permissions.html', {'message': 'There is no such order'})
        order = Order.objects.get(pk=order_id)
        if request.user.company_id != order.company_id:
            return render(request, 'admin/no_permissions.html', {'message': 'This is not your order!'})

        form = StatusForm(request.POST)
        if form.is_valid():
            order.status = form.cleaned_data['status']
            order.save()
            status = int(order.status)
            historic_entry(order_id, request.user, f"User set status: {STATUS_LIST[status][1]}")
            update_modification_time(order.id)
        return redirect(f'/panel/show-complaint/{order_id}/')