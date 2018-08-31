from django.contrib import admin

# Register your models here.

from .models import Issues

class IssuesModelAdmin(admin.ModelAdmin):
	list_display = ["title_issue","title_project","status"]
	list_display_link = ["title_project"]
	# list_editables = ["title"]
	# list_filter = ["date"]
	search_fields = ["title_issue","title_project","status"]
	class Meta: 
		model = Issues
 
admin.site.register(Issues,IssuesModelAdmin)

# class ProjectsModelAdmin(admin.ModelAdmin):
# 	list_display = ['title','mentor']
# 	class Meta: 
# 		model = Projects
		
# admin.site.register(Projects,ProjectsModelAdmin)
