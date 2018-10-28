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
import json
from .models import Issues, Prs
import time
from django.db.models import Q


def vote(request):
    if request.user.is_authenticated:
        issue_id= int(request.GET['issue_id'])
        vote_type = request.GET['type']

        issue = get_object_or_404(Issues, pk=issue_id)
        print(issue_id)
        print(issue.upvotes.count())
        print("inside votes")
        UserUpVote = issue.upvotes.filter(id=request.user.id).count()
        UserDownVote = issue.downvotes.filter(id=request.user.id).count()
        if (UserUpVote == 0) and (UserDownVote == 0):
            if (vote_type == 'up'):
                issue.upvotes.add(request.user)
            elif (vote_type == 'down'):
                issue.downvotes.add(request.user)
            else:
                return HttpResponse('error-unknown vote type')
        else:
            if (vote_type == 'up') and (UserUpVote == 1):
                issue.upvotes.remove(request.user)
            #When a user clicks downvote while he/she has already upvoted then upvote will dec by 1 and downvote will get updated
            elif (vote_type == 'down') and (UserUpVote==1):
                issue.upvotes.remove(request.user)
                issue.downvotes.add(request.user)
            elif (vote_type == 'up') and (UserDownVote == 1):
                issue.downvotes.remove(request.user)
                issue.upvotes.add(request.user)
            elif (vote_type == 'down') and (UserDownVote == 1):
                issue.downvotes.remove(request.user)
            else:
                return HttpResponse('error - unknown vote type or no vote to recall')
        upvotes_count = issue.upvotes.count()
        downvotes_count = issue.downvotes.count()

        count={'upvotes_count':upvotes_count,
            'downvotes_count':downvotes_count}

        return HttpResponse(json.dumps(count), content_type="application/json")
    else: return HttpResponseBadRequest()

def home(request):
    if request.method == 'GET':
        print('home GET')
		# Getting value of the clicked option
        val = request.GET.get('value','')
        print('val - ', val)
        # First it checks for project name
        if val and val != 'points':
            try:
                print("in the try block")
                val = int(val)
                issues = Issues.objects.filter(level = val)
            except Exception:
                print("in the except block")
                # status_filter = 
                if val[0]=='_':
                    temp_val=int(val[1]) #don't change this val as it's being passed to template
                    issues = Issues.objects.filter(label=temp_val)
                else:
                    project_filter = Issues.objects.filter(title_project=str(val))
                    mentor_filter  = Issues.objects.filter(mentor__username=str(val))
                    issues = project_filter or mentor_filter
            issues = issues.order_by('-pk')
        else:
            print("all issues|else block")
            if val and val == 'points':
                issues = Issues.objects.all().order_by('points')
            else:
                issues = Issues.objects.all().order_by('-pk')
        paginator = Paginator(issues, 15)  # Show 15 issues per page
        page = request.GET.get('page', 1)
        
        try:
            issues = paginator.get_page(page)
        except PageNotAnInteger:
            issues = paginator.get_page(1)
            # issues = paginator.get_page(1)
        except EmptyPage:
            issues = paginator.get_page(paginator.num_pages)
            issues = Issues.objects.none()
        return render(request, 'Projects/home.html', {'issues': issues, 'val':val }) #this dic will have value of
																					#all filter attributes or you can also send a list of all such attrs

def leaderboard(request):
    if request.method == 'GET':
        users = User.objects.all().filter(profile__role='student').order_by('-profile__points')
        paginator = Paginator(users,10)
        page = request.GET.get('page',1)
        try:
            users = paginator.get_page(page)
        except PageNotAnInteger:
            users = paginator.get_page(1)
        except EmptyPage:
            users = paginator.objects.none()
        time.sleep(0.5)
        return render(request, 'Projects/leaderboard.html', {'users': users})


@login_required(login_url='signin')
def profile(request, username):
	#solved issues are closed after verification
	#'student'-not attempted, 2-pending_for_verification, 3-verified_closed, 4-unverified_closed
	try:
		user = get_object_or_404(User, username=username)
	except: #this is a fix for a non existing source too
		return redirect("home")

	all_prs 		  = Prs.objects.all().filter(from_user=user)
	if request.user.profile.role=='student' and request.user == user:
		print('its a student', user.username)
		prs_vclosed       = Prs.objects.all().filter(from_user=user, status=3).order_by('-pk')
		prs_pending 	  = Prs.objects.all().filter(from_user=user, status=2).order_by('-pk')
		return render(request, 'Projects/profile.html', {
								'page_user' : user,
								'all_prs' : all_prs,
								'prs_pending': prs_pending,
								'prs_vclosed': prs_vclosed,
								})
	elif request.user.profile.role == 'mentor' and request.user.is_staff:
		print('its a mentor and staff status approved')
		all_prs			  = Prs.objects.all().filter(issue__mentor=user).order_by('-pk')
		prs_vclosed       = Prs.objects.all().filter(issue__mentor=user, status=3).order_by('-pk')
		prs_pending 	  = Prs.objects.all().filter(issue__mentor=user, status=2).order_by('-pk')
		print(len(prs_vclosed))
		return render(request, 'Projects/profile.html', {
								'page_user' : user,
								'all_prs' : all_prs,
								'prs_pending': prs_pending,
								'prs_vclosed': prs_vclosed,
								})
	else: return redirect("home")

def contri_user(request,username):
    user = get_object_or_404(User, username=username)
    prs_vclosed = Prs.objects.all().filter(from_user=user, status=3).order_by('-pk')
    prs_pending = Prs.objects.all().filter(from_user=user, status=2).order_by('-pk')
    return render(request, 'Projects/contribution_user.html', {
                                'prs_vclosed': prs_vclosed,
                                'prs_pending':prs_pending,
                                })


def request_pr(request):
    print('request_pr')
    if request.method=='POST' and request.user.profile.role=='student':
        issue_id = request.POST.get('issue_id')
        pr_link = request.POST.get('pr_link')
        print('issueid, pr_link',issue_id,pr_link)
        issue = get_object_or_404(Issues,id=issue_id)
        user=request.user
        message='Some unknow error has occured :('
        message_pr="No such issue"
        if issue:
            message_pr='Your request has been sent to the mentor for this issue, ' + issue.mentor.username + '. You will see the result of this PR shortly.'
            mentor = issue.mentor
            title_issue = issue.title_issue
            title_project = issue.title_project
            link_project = issue.link_project
            link_issue = issue.link_issue
            level = issue.level
            pr_link = pr_link


            exist_pr = Prs.objects.all().filter(issue=issue, from_user=user, status=2)
            if exist_pr:
                message_pr = "You  already have a pending PR for this issue. You can create PR"+\
                " again only after your current PR is reviewed. You should try contacting the issue mentor, "\
                + issue.mentor.username + " at "+ issue.mentor.email +"\n\nThank You."
            else:
                new_pr = Prs()
                new_pr.issue = issue
                new_pr.from_user = request.user
                new_pr.status = 2
                new_pr.pr_link = pr_link
                new_pr.all_such_prs = new_pr.all_such_prs+1
                new_pr.save()

                print('Created a new PR with pr_id',new_pr.id)

                from_email = django_settings.EMAIL_HOST_USER
                to_email = [issue.mentor.email]

                subject = request.user.username + ' has requested you accept PR'
                message = 'Hi '+ mentor.username + '!' + '<br>' + 'Here is a request for verifying a PR which you mentor.<br>'\
                        'Issue - <a href="' + link_issue+ '">' + title_issue + '</a><br>' +\
                        'Project - <a href="' + link_project + '">' + title_project + '</a><br>' +\
                        'Check the PR here - <a href="' + pr_link + '">PR</a><br>' +\
                        'You can also visit your <a href="https://contrihubs.herokuapp.com/'+ issue.mentor.username +'"> profile </a> to see all pending requests and accept or reject them.<br><br>Cheers!!!'
                        # 'Label - '+ level +'<br>'+\

                send_mail(subject, message, from_email, to_email, fail_silently=False, html_message=message)
        print(message_pr)
        return HttpResponse(message_pr)
    else: return HttpResponse("You should be a student for making PRs")


def response_pr(request):
    if request.method=='POST' and request.user.profile.role=='mentor':
        pr_id = request.POST.get('pr_id')
        pr = get_object_or_404(Prs, id=pr_id)
        bonus_pts=request.POST.get('bonus_pts','0')
        deducted_points=request.POST.get('deduct_pts','0')
        bonus_pts=int(bonus_pts)
        deducted_points=int(deducted_points)
        print("bonus - ",bonus_pts)
        print("deduct - ",deducted_points)
        #1-not attempted, 2-pending_for_verification, 3-verified_closed, 4-unverified_closed
        if pr:
            print(pr.issue.mentor.username)
            print('Changing the status of PR')
            print('pr_status',pr.status)
            if pr.status==2:
                pr.status=3
                print(deducted_points)
                print(pr.from_user.profile.deducted_points)
                #total points of pr making user
                pr.from_user.profile.points=pr.from_user.profile.points+pr.issue.points+bonus_pts-deducted_points
                
                #modifying bonus and deducted points for pr making user
                pr.from_user.profile.bonus_points = pr.from_user.profile.bonus_points+bonus_pts
                pr.from_user.profile.deducted_points = pr.from_user.profile.deducted_points+deducted_points
                
                #modifying pr bonus and deducted points
                pr.bonus_points = pr.bonus_points+ bonus_pts
                pr.deducted_points = pr.deducted_points + deducted_points
                
                subject = pr.issue.mentor.username + ' has verified your PR'
                var_msg = 'Congratulations. Your pull request has been verified by mentor, '
                # print('Changing the status to', 3 ,'and points to',pr.from_user.profile.points)
                print(pr.from_user.profile.deducted_points)
            elif pr.status==3:
                pr.status=2
                #total points of pr making user
                pr.from_user.profile.points=pr.from_user.profile.points-(pr.issue.points+pr.bonus_points-pr.deducted_points)
                
                #modifying bonus and deducted points for pr making user
                pr.from_user.profile.bonus_points = pr.from_user.profile.bonus_points-pr.bonus_points
                pr.from_user.profile.deducted_points = pr.from_user.profile.deducted_points-pr.deducted_points
                
                #modifying pr bonus and deducted points
                pr.bonus_points=0
                pr.deducted_points=0
                
                subject = pr.issue.mentor.username + ' has rejected your PR'
                var_msg = 'Your pull request has been rejected by mentor, '
            pr.save()
            pr.from_user.save()
            print('pr_status',pr.status)

            from_email = django_settings.EMAIL_HOST_USER
            to_email = [pr.from_user.email] #I'm not sure what the request object looks like so this may not be the correct notation

            print(pr.from_user.username)
            message = 'Hi '+ pr.from_user.username + '!' + '<br>' +\
                     var_msg +\
                     pr.issue.mentor.username + '.<br>'+\
                    'Issue - <a href="'+pr.issue.link_issue+'">'+pr.issue.title_issue+'</a><br>'+\
                    'Project - <a href="'+pr.issue.link_project+'">'+pr.issue.title_project+'</a><br>'+\
                    'Check the PR here - <a href="'+pr.pr_link+'">PR</a><br>'+\
                    'You can also visit your <a href="https://contrihubs.herokuapp.com/'+ pr.from_user.username +'"> profile </a> to see all pending/rejected requests.<br><br>Cheers!!!'
            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False, html_message=message)
                # print()
            except Exception:
                pass
        else: print('PR doesn\'t exist')
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
        print('Searching if such PR exists with id',pr_id)
        pr = get_object_or_404(Prs, id=pr_id)
        print("PR ID is",pr_id,user.username,pr.from_user.username)
        if pr.from_user == user or user.is_staff :
            pr.delete()
            response="Successfully deleted this PR."
        else:
            response="You didn't create this PR. So this can not be deleted by you. Sorry :("
  
        return HttpResponse(response)


def change_label(request):
    if request.user.is_authenticated and request.method == 'POST' and request.user.profile.role == 'mentor':
        res=""
        print('closing issue')
        issue_id = request.POST.get('issue_id')
        try:
            issue = get_object_or_404(Issues, id=issue_id)
        except expression as identifier:
            return HttpResponseBadRequest()
        if issue.label == 1:
            issue.label = 0
            res="closed the issue "+issue.title_issue
        else:
            issue.label = 1
            res="opened the issue "+issue.title_issue
        issue.save()
        return HttpResponse(res)
    else: return HttpResponseBadRequest()

def new_issue(request):
    print('adding issue')
    if request.method == 'POST' and request.user.is_staff:
        print('in add issue method')
        mentor_name_issue   = request.POST.get('mentor_name_issue')
        title_issue         = request.POST.get('title_issue')
        link_issue         = request.POST.get('link_issue')
        title_project       = request.POST.get('title_project')
        link_project        = request.POST.get('link_project')
        try:
            level  = int(request.POST.get('level'))
            points = int(request.POST.get('points'))
        except Exception:
            error_add_issue = 'level or points not an integer'
        try:
            mentor = get_object_or_404(User, username=mentor_name_issue)
        except Exception:
            error_add_issue = "Mentor doesn't exist"
        
        if not error_add_issue:
            new_issue = Issues()
            new_issue.mentor = mentor
            new_issue.title_issue = title_issue
            new_issue.link_issue = link_issue
            new_issue.title_project = title_project
            new_issue.link_project = link_project
            new_issue.level = level
            new_issue.points = points
            new_issue.save()
            return redirect('home')
        else:
            issues=Issues.objects.all().order_by('-id')
            paginator = Paginator(issues, 15)  # Show 15 issues per page
            page = request.GET.get('page', 1)
            return redirect('home', error_add_issue=error_add_issue)            
    else:
        error_add_issue = "Not a staff"
        return redirect('home', error_add_issue=error_add_issue)

