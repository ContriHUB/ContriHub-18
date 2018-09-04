from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages  
from django.conf import settings as django_settings  
from django.core.mail import send_mail 
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden) 
   
 
def signin(request):
    print('inside authentication.view') 
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.all().filter(username=username)
        if user:
            print('user exists')
            user = User.objects.all().filter(username=username)[0]
            # if not user.is_active:
            #     error_inactive = True
            #     return render(request,'registration/login.html',{'error_inactive':error_inactive})            
            # else:
            login(request, user)
            return redirect('home')
        if not user:
            error_signin = True
            return render(request,'registration/login.html',{'error_signin':error_signin})

    else: return render(request,'registration/login.html',{})

def register(request):
    print('inside register authentication.view') 
    
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        role = request.POST.get('role')

        user = User.objects.all().filter(username=username)
        if user:
            error_register = True
            return render(request,'registration/login.html',{'error_register':error_register})
        if not user:
            print('No user exists')
            User.objects.create_user(username=username, password=password, email=email)  # removed email at signup to make signup fast
            user = authenticate(username=username, password=password)           

            user.profile.gender = gender
            if role=='student': user.profile.role = 'student'
            else:
                user.profile.role = 'mentor'

            user.save()
            login(request, user)
            return redirect('home')

            # user.profile.gender = gender
    else: return render(request,'registration/login.html',{})
