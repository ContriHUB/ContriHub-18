from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden) 
from django.template.context_processors import csrf  
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Issues,Prs

def home(request):
	issues = Issues.objects.all().order_by('points')
	paginator = Paginator(issues, 4)  # Show 25 contacts per page
	page = request.GET.get('page')
	issues = paginator.get_page(page)

	return render(request, 'Projects/home.html', {'issues': issues})

def leaderboard(request):
	users = User.objects.all().filter(profile__role='student').order_by('-profile__points')
	paginator = Paginator(users,4)
	page = request.GET.get('page')
	users = paginator.get_page((page))
	return render(request, 'Projects/leaderboard.html', {'users':users} )

@login_required(login_url='signin')
def profile(request, username):
	#solved issues are closed after verification
	#'student'-not attempted, 2-pending_for_verification, 3-verified_closed, 4-unverified_closed
	user = get_object_or_404(User, username=username)
	all_prs 		  = Prs.objects.all().filter(from_user=user)
	if request.user.profile.role=='student':
		print('its a student', user.username)
		prs_nattempted    = Prs.objects.all().filter(from_user=user, status=1)
		prs_vclosed       = Prs.objects.all().filter(from_user=user, status=3)
		prs_unvclosed     = Prs.objects.all().filter(from_user=user, status=4)
		prs_pending 	  = Prs.objects.all().filter(from_user=user, status=2)
		print(len(prs_nattempted),len(prs_vclosed))
		return render(request, 'Projects/profile.html', {
								'page_user' : user,
								'all_prs' : all_prs,
								'prs_not_attempted': prs_nattempted,
								'prs_pending': prs_pending,
								'prs_vclosed': prs_vclosed,
								'prs_unvclosed': prs_unvclosed,
								}) 
	else:
		print('its a mentor')
		all_prs			  = Prs.objects.all().filter(issue__mentor=user)
		prs_vclosed       = Prs.objects.all().filter(issue__mentor=user, status=3)
		prs_unvclosed     = Prs.objects.all().filter(issue__mentor=user, status=4)
		prs_pending 	  = Prs.objects.all().filter(issue__mentor=user, status=2)
		print(len(prs_vclosed))
		return render(request, 'Projects/profile.html', {
								'page_user' : user,
								'all_prs' : all_prs,
								'prs_pending': prs_pending,
								'prs_vclosed': prs_vclosed,
								'prs_unvclosed': prs_unvclosed,
								}) 

 
def request_pr(request):
	print('request_pr')
	if request.method=='POST' and request.user.profile.role=='student':
		issue_id = request.POST.get('issue_id')
		pr_link = request.POST.get('pr_link')
		print('issueid, pr_link',issue_id,pr_link)
		issue = get_object_or_404(Issues,id=issue_id)
		user=request.user
		message='some unknow error occured error :('
		message_pr="No Such Issue"
		if issue:
			message_pr='Your request has been sent to '+issue.mentor.username+', mentor of this issue, soon you will see result of this PR'
			mentor = issue.mentor
			title_issue = issue.title_issue
			title_project = issue.title_project
			link_project = issue.link_project
			link_issue = issue.link_issue
			level = issue.level 
			pr_link = pr_link
 
			
			exist_pr = Prs.objects.all().filter(issue=issue, from_user=user, status=2)
			if exist_pr:
				message_pr = "You have already a pending pr for this issue. You can create PR"+\
				" again only after your current PR is reviewed. You should try contacting Issue mentor "\
				+ issue.mentor.username + " at "+ issue.mentor.email +"\nThank You."
			else:
				new_pr = Prs()
				new_pr.issue = issue
				new_pr.from_user = request.user
				new_pr.status = 2
				new_pr.pr_link = pr_link
				new_pr.all_such_prs = new_pr.all_such_prs+1 
				new_pr.save()

				print('created a new pr with pr_id',new_pr.id)
				
				from_email = django_settings.EMAIL_HOST_USER
				to_email = [issue.mentor.email]

				subject = request.user.username + ' has requested to accept pr '
				message = 'Hi '+mentor.username +' !'+'<br>'+'Here is a request for verifying a pr which you are mentoring.<br>'\
						'Issue - <a href="'+link_issue+'">'+title_issue+'</a><br>'+\
						'Project - <a href="'+link_project+'">'+title_project+'</a><br>'+\
						'Check the pr here - <a href="'+pr_link+'">PR</a><br>'+\
						'You can also visit your profile to see all pending requests and accept or reject them.<br><br>Cheers!!!'
						# 'Label - '+ level +'<br>'+\

				send_mail(subject, message, from_email, to_email, fail_silently=False, html_message=message)        
		print(message_pr)
		return HttpResponse(message_pr)
	else: return HttpResponse("You should be a student for making PRS")


def response_pr(request):
	if request.method=='POST' and request.user.profile.role=='mentor':
		pr_id = request.POST.get('pr_id')
		pr = get_object_or_404(Prs, id=pr_id)

		#1-not attempted, 2-pending_for_verification, 3-verified_closed, 4-unverified_closed
		if pr:
			print('changing the status of pr')
			print('pr_status',pr.status)
			if pr.status==2:
				pr.status=3
				pr.from_user.profile.points=pr.from_user.profile.points+pr.issue.points
				print('changing the status to', 3 ,'and points to',pr.from_user.profile.points)
			elif pr.status==3:
				pr.status=2
				pr.from_user.profile.points=pr.from_user.profile.points-pr.issue.points
			pr.save()
			pr.from_user.save()
			print('pr_status',pr.status)
		else: print('pr doesnt exist')
	return HttpResponse("success")

def remove_issue(request):
	print('inside delete issue')
	user=request.user
	response=""
	if request.method=="POST":
		issue_id=request.POST.get('issue_id')
		issue = get_object_or_404(Issues, id=issue_id)
		if issue.mentor == user:
			issue.delete()
			response="Successfully deleted the issue."
		else:
			response="You didn't create this issue.So this can not be deleted by you. Sorry :("
		
		return HttpResponse(response)

def remove_pr(request):
	print('inside delete pr')
	user=request.user
	response=""
	if request.method=="POST":
		pr_id=request.POST.get('pr_id')
		print('searching if such pr exists with id',pr_id)
		pr = get_object_or_404(Prs, id=pr_id)
		print("pr id is",pr_id,user.username,pr.from_user.username)
		if pr.from_user == user:
			pr.delete()
			response="Successfully deleted this PR."
		else:
			response="You didn't create this PR.So this can not be deleted by you. Sorry :("
		
		return HttpResponse(response)

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

