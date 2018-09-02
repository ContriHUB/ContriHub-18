from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import post_save 

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True) 
    is_student = models.IntegerField(_('is_student'), default=1) #1-student, 2-mentor 
    first_name = models.CharField(_('first_name'), max_length=40, blank=True, null=True) 
    last_name = models.CharField(_('last_name'), max_length=40, blank=True, null=True)
    bio = models.CharField(_('status'), max_length=100, blank=True, null=True) 
    points = models.IntegerField(_('points'), default=0)
    rank = models.IntegerField(_('rank'), default=0)
    gender = models.CharField(_('gender'), max_length=7, blank=True, null=True) 

    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return 'User - {}, Rank - {}, Bio - {}'.format(self.user.username, self.rank, self.bio)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

