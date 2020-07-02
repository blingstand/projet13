""" this script manages the views """
# global
import random, string

#django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


#from current app import
from .form import UserForm
# from .utils import MailAgent, notify_db_fv, get_user_and_profile, add_new_user
from .utils import add_new_user


# class ConnectionView(TemplateView):
#     template_name = "user/connection.html"
    
#     def get(self, request, **kwargs):
#         return render(request, self.template_name)

class RegisterView(View):
    """ This class deals with registration
        get > loads a registration page
        post > analyses datas to try to create a new user and profile
    """

    def get(self, request):
        """ manages the get request for the register page """
        if request.user.is_authenticated:
            return redirect('dashboard:index') #if auth user comes to register page
        us_form = UserForm()
        context = {'us_form': us_form}
        return render(request, 'user/register.html', context)

    def post(self, request):
        """
        manages the post request for the register page :
            get datas in order to try to create a new user

        """
        us_form = UserForm(request.POST)
        if us_form.is_valid():
            name, password = us_form.cleaned_data['username'], us_form.cleaned_data['password']
            success, message = add_new_user(name, password)
            messages.info(request, message)
            if success:
                return redirect('user:connection')
            return redirect('user:register')
        return HttpResponse("Problème dans le formulaire !")


class ConnectionView(View):
    """ This class deals with login
        get > loads a connection page
        post > analyses datas in order to try to authenticate
    """
    def get(self, request):
        """ manage the get request concerning the connection page """
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        us_form = UserForm()
        context = {'us_form' : us_form}
        return render(request, 'user/connection.html', context)

    def post(self, request):
        """
        manages the post request for connection page,  use given datas
        in order to try to authenticate
        """
        us_form = UserForm(request.POST)
        if us_form.is_valid():
            username = us_form.cleaned_data['username']
            password = us_form.cleaned_data['password']
            new_user = authenticate(username=username, password=password)

            if new_user is not None:
                login(request, new_user)
                return HttpResponse('Vous êtes co')
                return redirect('dashboard:index')
            messages.info(request, 'Pseudo ou mot de passe incorrect')
            return redirect('user:connection')
        return HttpResponse("Problème dans le formulaire !")


class LogoutUser(View):
    """ manages the sign out function"""
    def get(self, request):
        """ manages the get request for the logout page"""
        logout(request)
        return redirect('user:connection')
        