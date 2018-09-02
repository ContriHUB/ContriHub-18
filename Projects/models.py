from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


# Create your models here.

# class Projects(models.Model):
#     issue  = models.ForeignKey("Issues", verbose_name=_("issues"), db_column="issue", on_delete=models.CASCADE)
#     title  = models.CharField(_('project_title'), max_length=40, blank=True, null=True)
#     mentor = models.CharField(_('mentor_of_project'), max_length=30, blank=True, null=True)
#     # level  = models.IntegerField(_('level_of_project'), default=1)

#     class Meta:
#         db_table = 'projects_for_issues'
#         managed = True
#         verbose_name = 'project'
#         verbose_name_plural = 'projects'

#     def __str__(self):
#         return 'Project - {}, Mentor - {}'.format(self.title,self.mentor)


class Issues(models.Model):
    # project = models.ForeignKey("Projects.Projects", verbose_name=_("projects"), db_column="project_title", on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title_issue = models.CharField(_('title_issue'), max_length=40, blank=True, null=True)
    link_issue = models.CharField(_('link_issue'), max_length=200, blank=True, null=True)

    title_project = models.CharField(_('title_project'), max_length=40, blank=True, null=True)
    link_project = models.CharField(_('link_project'), max_length=200, blank=True, null=True)

    level  = models.IntegerField(_('level_issue'), default=1) #1-easy, 2-medium, 3-difficult 
    status = models.IntegerField(_('status_issue'), default=1) 
    #1-not attempted, 2-pending_for_verification, 3-verified_closed, 4-unverified_closed 

    class Meta:
        db_table = 'issues_info'
        managed = True
        verbose_name = 'issue'
        verbose_name_plural = 'issues'

    def __str__(self):
        return 'Issue - {}, Project - {}, Mentor - {}'.format(self.title_issue, self.title_project,self.mentor.username)


class Prs(models.Model):
    issue     = models.ForeignKey("Projects.Issues", on_delete=models.SET_NULL, null=True)
    from_user = models.ForeignKey(User, related_name="user_who_creates_pr", on_delete=models.SET_NULL, null=True)
    all_prs   = models.IntegerField(_('all_such_prs'), default=1)

    class Meta:
        db_table = 'prs_info'
        managed = True
        verbose_name = 'pr'
        verbose_name_plural = 'prs'

    def __str__(self):
        return '{} created a pr for {}'.format(self.from_user.username,self.issue.title_issue)
