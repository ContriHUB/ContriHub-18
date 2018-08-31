from django.db import models

# Create your models here.

class Projects(models.Model):
    issue  = models.ForeignKeyField("Issues", verbose_name=_("issues"), db_column="issue", on_delete=models.CASCADE)
    title  = models.CharField(_('project_title'), max_length=40, ${blank=True, null=True})
    mentor = models.CharField(_('mentor_of_project'), max_length=30, ${blank=True, null=True})
    level  = models.IntegerField(_('level_of_project'), default=1)

    class class Meta:
        db_table = 'projects_for_issues'
        managed = True
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def __str__(self):
        return 'Project - {}, Mentor - {}'.format(self.title,self.mentor)


class Issues(models.model):
    project = models.ForeignKeyField("Projects.Projects", verbose_name=_("projects"), db_column="project_title", on_delete=models.CASCADE)
    title = models.CharField(_('issue_title'), max_length=length, ${blank=True, null=True})
    level  = models.IntegerField(_('level_of_issue'), default=1)
    status = models.IntegerField(_('level_of_issue'), default=0)

    class class Meta:
        db_table = 'issues_info'
        managed = True
        verbose_name = 'issue'
        verbose_name_plural = 'issues'

    def __str__(self):
        return 'Issue - {}, Project - {}, Mentor - {}'.format(self.title, self.project.title,self.project.mentor)


