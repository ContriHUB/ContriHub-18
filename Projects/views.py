from django.shortcuts import render
from .models import Issues
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden) 
from django.template.context_processors import csrf  
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.shortcuts import get_object_or_404, render, redirect


def home(request):
    issues = Issues.objects.all()
    return render(request, 'Projects/home.html', {'issues':issues})


def request_pr(request):
	print('request_pr')
	if request.method=='POST':
		issue_id = request.POST.get('issue_id')
		print('issueid',issue_id)
		issue = get_object_or_404(Issues,id=issue_id) 

		mentor = issue.mentor
		title_issue = issue.title_issue
		title_project = issue.title_project
		link_issue = issue.link_issue
		level = issue.level 
		
		from_email = django_settings.EMAIL_HOST_USER
		# to_email = issue.

		subject = request.user + ' has requested to accept pr '
		message = 'Hi '+mentor +' !'+'<br>'+'Here is a request for merging a pr which you are mentoring.<br>'\
				  'Issue - <a href="'+link_issue+'">'+title_issue+'</a><br>'+\
				  'Project - <a href="'+link_project+'">'+title_project+'</a><br>'+\
				  'Label - '+ level +'<br>'+\
				  'You can also visit your profile to see all pending requests and accept or reject them<br>'

		send_mail(subject, message, from_email, to, fail_silently=False,html_message=message)        

		return HttpResponse("success")


# def add_issue(request):
#     if request.method=='POST':
#         title_issue=request.POST.get('title_issue')
#         link_issue=request.POST.get('issue_link')
#         title_project=request.POST.get('title_project')
#         link_issue=request.POST.get('link_project')

#         level_issue=request.POST.get('level')

#         issue = Issues()
#         issue.title_issue=title__issue
#         issue.link_issue=link_issue
#         issue.title_project=title_project
#         issue.link_project=link_project
#         issue.level_issue=level_issue
#         issue.mentor=request.user.username

#         issue.save()
#     else:
#         return redirect('home')

