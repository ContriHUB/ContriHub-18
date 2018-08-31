from django.contrib import admin

# Register your models here.
from .models import Profile

class ProfileModelAdmin(admin.ModelAdmin):
	list_display = ["first_name","rank","bio"]
	search_fields = ["rank","first_name"]

	class Meta: 
		model = Profile
 
admin.site.register(Profile,ProfileModelAdmin)


