"""ContriHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static  
from django.contrib.auth.views import (LoginView, LogoutView)

from Projects.views import (home,request_pr,response_pr,leaderboard,profile,remove_issue,remove_pr,contri_user,switch_label)

from Users.views import (signin,register)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('cooladmins', admin.site.urls),
    path('', home, name='home'),
    path('signin', signin , name='signin'),
    path('signup', register , name='register'), 
    path('logout', LogoutView.as_view(), {'next_page': 'signin'}, name='logout'),

    # path('api/github_webhook/', views.github_webhook, name='github_webhook')
    path('request_pr', request_pr , name='request_pr'),
    path('response_pr', response_pr , name='response_pr'),

    path('leaderboard', leaderboard , name='leaderboard'),     
    path('remove_issue', remove_issue , name='remove_issue'),
    path('remove_pr', remove_pr , name='remove_pr'),

    path('switch_label', switch_label , name='switch_label'),

    #put such urls always after all
    path('<username>', profile, name='profile'),
    path('contributions/<username>', contri_user, name='contri_user'),
    
    # password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
# (?P<username>[^/]+)/

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
   
