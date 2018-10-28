from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, null=True) 
    role            = models.CharField(_('user_role'), max_length=10, blank=True, null=True)
    first_name      = models.CharField(_('first_name'), max_length=40, blank=True, null=True) 
    last_name       = models.CharField(_('last_name'), max_length=40, blank=True, null=True)
    bio             = models.CharField(_('bio'), max_length=100, blank=True, null=True) 
    points          = models.IntegerField(_('points'), default=0)
    rank            = models.IntegerField(_('rank'), default=0)
    gender          = models.CharField(_('gender'), max_length=7, blank=True, null=True)
    college         = models.CharField(_('college_name'), max_length=100, blank=True, null=True)
    issues_solved   = models.IntegerField(_('issues_solved'), default=0)
    country         = models.CharField(_('country'), max_length=20, blank=True, null=True)
    bonus_points    = models.IntegerField(_('bonus_points'),default=0)
    deducted_points = models.IntegerField(_('deducted_points'),default=0)
    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        if self.user:
            return 'User - {}, Rank - {}, Bio - {}'.format(self.user.username, self.rank, self.bio)
        else: return str(self.rank)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    if instance.profile:  
        instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

