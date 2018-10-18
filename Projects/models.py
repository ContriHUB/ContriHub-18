from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class Issues(models.Model):
    # project = models.ForeignKey("Projects.Projects", verbose_name=_("projects"), db_column="project_title", on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title_issue = models.CharField(_('title_issue'), max_length=40, blank=True, null=True)
    link_issue = models.CharField(_('link_issue'), max_length=200, blank=True, null=True)

    title_project = models.CharField(_('title_project'), max_length=40, blank=True, null=True)
    link_project = models.CharField(_('link_project'), max_length=200, blank=True, null=True)

    level  = models.IntegerField(_('level_issue'), default=1) #1-easy, 2-medium, 3-difficult 
    points = models.IntegerField(_('points_for_issue'), default=0)
    class Meta:
        db_table = 'issues_info'
        managed = True
        verbose_name = 'issue'
        verbose_name_plural = 'issues'

    def __str__(self):
        return 'Issue - {}, Project - {}, Mentor - {}'.format(self.title_issue, self.title_project,self.mentor.username)


class Prs(models.Model):
    issue     = models.ForeignKey("Projects.Issues", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name="user_who_creates_pr", on_delete=models.CASCADE, null=True)
    all_such_prs   = models.IntegerField(_('all_such_prs'), default=1)
    status    = models.IntegerField(_('status_issue'), default=1) 
    pr_link   = models.CharField(_('pr_issue'), max_length=200, blank=True, null=True)
    #1-not attempted, 2-pending_for_verification, 3-verified_closed, 4-unverified_closed 

    class Meta:
        db_table = 'prs_info'
        managed = True
        verbose_name = 'pr'
        verbose_name_plural = 'prs'

    def __str__(self):
        if self.from_user:
            return '{} created a pr for {}'.format(self.from_user.username,self.issue.title_issue)
        else: return str(self.issue.title_issue)


#on_delete attr tells what to do with this object when the model current object is referring is deleted
#on_delete=models.CASCADE , deletes current model when referred object is deleted
#on_delete=SET_NULL  , sets the foreign key in current object to NULL

