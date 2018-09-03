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

from Projects.views import (home,request_pr,response_pr,leaderboard, profile)
from Users.views import (signin,register)

urlpatterns = [
    path('admin', admin.site.urls),
    path('', home, name='home'),
    path('signin', signin , name='signin'), 
    path('register', register , name='register'), 
    path('logout', LogoutView.as_view(), {'next_page': 'signin'}, name='logout'),

    # path('api/github_webhook/', views.github_webhook, name='github_webhook')
    path('request_pr', request_pr , name='request_pr'),
    path('response_pr', response_pr , name='response_pr'),

    path('leaderboard', leaderboard , name='leaderboard'),     
    path('<username>', profile, name='profile'),
]
# (?P<username>[^/]+)/

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
   