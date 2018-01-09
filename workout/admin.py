from django.contrib import admin
from .models import ActivityType, Workout

admin.site.register(ActivityType)

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['member', 'primary_type', 'performed_date', 'registered_date']
    
admin.site.register(Workout, WorkoutAdmin)