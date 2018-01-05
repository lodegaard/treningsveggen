from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class ActivityType(models.Model):
    name = models.CharField(max_length=200)
    human_readable = models.CharField(max_length=200)
    
    def __str__(self):
        return self.human_readable
    
    def get_all_activity_types(self):
        return 0

class Workout(models.Model):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    
    performed_date = models.DateField('Performed')
    registered_date = models.DateTimeField('Registered')
    
    primary_type = models.ForeignKey(
        ActivityType,
        on_delete=models.DO_NOTHING,
        related_name='primary',
        null=False
    )
    secondary_type = models.ForeignKey(
        ActivityType,
        on_delete=models.DO_NOTHING,
        related_name='secondary',
        blank=True,
        null=True,
    )
     
    comment = models.CharField(max_length=500)
    fb_post_id = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        if self.secondary_type is not None:
            return str(self.primary_type) + '/' + str(self.secondary_type)
        else:
            return str(self.primary_type)

    def get_latest(self):
        return Workout.objects.all()[:10]
    
    def number_in_week(self):
        today = datetime.now()
        return self.member.workout_set.filter(performed_date__week=today.isocalendar()[1]).count()
        
        
        