from django.contrib import admin

# Register your models here.

from .models import Issues, Prs

class IssuesModelAdmin(admin.ModelAdmin):
	# list_display = ["title_issue","title_project","status"]
	# list_display_link = ["title_project"]
	# list_editables = ["title"]
	# list_filter = ["date"]
	# search_fields = ["title_issue","title_project","status"]
	class Meta: 
		model = Issues
 
class PrsModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Prs 

admin.site.register(Prs,PrsModelAdmin)
admin.site.register(Issues,IssuesModelAdmin)

# class ProjectsModelAdmin(admin.ModelAdmin):
# 	list_display = ['title','mentor']
# 	class Meta: 
# 		model = Projects
		
# admin.site.register(Projects,ProjectsModelAdmin)
