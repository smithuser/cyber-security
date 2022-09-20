from django.db import IntegrityError, transaction
from time import timezone
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from . import models
from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session

# Create your views here.

def index(request):
    return render(request, 'airportmgt/home.html')


def show_login(request):
    return render(request, 'airportmgt/login.html')


def show_signup(request):
    return render(request, 'airportmgt/register.html')

def signup(request:HttpRequest):
    if request.method == 'POST':
        if not request.POST['email'] or not request.POST['password'] or not request.POST['password_confirm'] or not request.POST['username']:
            messages.warning(request, 'Incomplete registration details!')
            return render(request, 'airportmgt/register.html')
        
        password1 = request.POST['password']
        password2 = request.POST['password_confirm']

        if password1 != password2:
            messages.warning(request, 'Passwords do not match!')
            return render(request, 'airportmgt/register.html')
        
        try:
            user = models.AppUser.objects.get(email=request.POST['email'])
            
            messages.warning(request, 'Email already exists')
            return render(request, 'airportmgt/register.html')
        except models.AppUser.DoesNotExist:
            pass
        



        try:
            user = models.AppUser.objects.get(username=request.POST['username'])
            
            messages.warning(request, 'Username already exists')
            return render(request, 'airportmgt/register.html')
        except models.AppUser.DoesNotExist:
            pass

        try:
            with transaction.atomic():
                user = models.AppUser.objects.create(email = request.POST['email'], username = request.POST['username'], password = password1)

                user.set_password(user.password)
                user.save()
                
                messages.success(request, 'Registration Successful! Please login with your details!')
                return render(request, 'airportmgt/login.html')

        except ValueError as e:
            messages.warning(request, 'User not created! ' + e)
            return render(request, 'airportmgt/register.html')


def login(request:HttpRequest):
    if request.method == 'POST':
        if not request.POST['email'] or not request.POST['password']:
            messages.warning(request, 'Invalid login credentials.')
            return render(request, 'airportmgt/login.html')
        
        # user = authenticate(email=request.POST['email'], password=request.POST['password'])
        try: 
            user = models.AppUser.objects.get(email=request.POST['email'])
            if not user.check_password(request.POST['password']):

                if user.failed_login_tries >= 4:
                    if not user.suspension_expires:
                        user.suspension_expires = datetime.now() + timedelta(days=2)
                        user.status = 'Inactive'
                        user.save()

                        return render(request, 'airportmgt/user_suspended.html', {'user': user})
                    elif datetime.now() > user.suspension_expires:
                        user.failed_login_tries = 0
                        user.suspension_expires = None
                        user.save()
                        
                        return render(request, 'airportmgt/login_success.html', {'username':user.username})
                    else:
                        return render(request, 'airportmgt/user_suspended.html', {'user': user})

                user.failed_login_tries += 1
                user.save()

                trials_remaining = 5 - user.failed_login_tries
                message = "Invalid login credentials! " + str(trials_remaining) + " trials remaining!"
                messages.warning(request, message)

                return render(request, 'airportmgt/login.html')

            if user.suspension_expires is not None:
                return render(request, 'airportmgt/user_suspended.html', {'user': user})

            if user.failed_login_tries > 0:
                user.failed_login_tries = 0
                user.save()

            if user.is_admin:
                banned_macs = get_banned_macs(user)
                return render(request, 'airportmgt/banned_addresses.html', {'username':user.username, 'banned_macs':banned_macs})

            return render(request, 'airportmgt/login_success.html', {'username': user.username})
        except models.AppUser.DoesNotExist:
            messages.warning(request, 'Invalid login credentials')
            return render(request, 'airportmgt/login.html')

def logout(request:HttpRequest):
    if request.method == 'POST':
        if request.POST['username']:
            try:
                user = models.AppUser.objects.get(username__exact=request.POST['username'])

                [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]

                user.is_active = False
                user.save()

                messages.success(request, 'Logout successful!')
                return redirect('/mgt/login/')
            except models.AppUser.DoesNotExist:
                pass

def get_banned_macs(user:models.AppUser):
    if user.is_admin and user.suspension_expires is None:
        return models.BannedMac.objects.order_by('id').all()