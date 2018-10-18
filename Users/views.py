from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages  
from django.core.mail import send_mail
from django.conf import settings as django_settings  
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden) 
import random
 
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
    print('inside authentication.view') 
    
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

def forgot_pass(request):
    global user_name
    if request.method == 'POST': 
        user_name = request.POST.get('username')
        
        user = User.objects.all().filter(username=user_name)
        if user:
            global verify_code
            print('user exists ')
            email = User.objects.all().filter(username=user_name).values('email')
            print(email[0].get('email'))
            verify_code = random.randint(5000, 9999)
            message = 'Hi ' + user_name + '\n' + 'Your verification code is : \n' + str(verify_code)
            from_email = django_settings.EMAIL_HOST_USER
            send_mail('Password Change', message, from_email, [str(email[0].get('email'))], fail_silently = False)
            mail_sent = True
            return render(request,'registration/login.html',{'mail_sent':mail_sent})
        if not user:
            error_username_verify = True
            return render(request,'registration/login.html',{'error_username_verify':error_username_verify})

    else: return render(request,'registration/login.html',{})
    
def verify(request):
    if request.method == 'POST':
        code_entered = request.POST.get('code')
        print(code_entered)
        if code_entered == str(verify_code):
            verified = True
            return render(request,'registration/login.html',{'verified':verified})
        else:
            not_verified = True
            return render(request,'registration/login.html',{'not_verified':not_verified})
        
def change_pass(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        print(new_password)
        #print(User.objects.all().filter(username=user_name))
        u = User.objects.get(username=user_name)
        u.set_password(new_password)
        u.save()
        pass_changed = True
        return render(request,'registration/login.html',{'pass_changed':pass_changed})
