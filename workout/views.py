from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import timezone

from django_facebook.api import get_persistent_graph

from .models import ActivityType, Workout

from datetime import date, datetime

import logging
log = logging.getLogger(__name__)

def get_activityTypes():
    return ActivityType.objects.all().exclude(name__contains='activity')

def get_workouts():
    return Workout.objects.all()

@login_required(login_url='/')
def list_workouts(request):
    today = datetime.now()
    member = request.user
    
    template = loader.get_template('workout/list.html')
    context = {
        'number_of_workouts': member.workout_set.filter(performed_date__week=today.isocalendar()[1]).count(),
        'workout_list': member.workout_set.all().order_by('-performed_date')[:50]
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/')
def add_workout(request):
    """
    """
    try:
        template = loader.get_template('treningsveggen/index.html')
        log.error("Received add workout form {}".format(request.POST))
        
        activity_type = ActivityType.objects.get(pk=request.POST['activity_type'])
        performed_date = request.POST['performed_date'].split('-')
        comment = request.POST['comment']
        performed = date(int(performed_date[0]), int(performed_date[1]), int(performed_date[2]))
        registered = timezone.now()
        
        newWorkout = Workout(member=request.user, performed_date=performed, registered_date=registered, primary_type=activity_type, comment=comment)
        newWorkout.save()
        
        fb_message = '{}. {} - {}'.format(newWorkout.number_in_week(), str(newWorkout), newWorkout.comment)
        post_to_fb = request.POST.get('post_to_fb', default=False)
        if post_to_fb:
            try:
                graph = get_persistent_graph(request)
                fb_group_id = settings.TRENINGSVEGGEN_FB_GROUP_ID
                post_result = graph.set('/{}/feed'.format(fb_group_id), {"message":fb_message})
                newWorkout.fb_post_id = post_result
            except:
                context = {
                    'info_messages': [fb_message],
                    'error_messages': ['Unable to post to Facebook, session expired. Please log in again']
                }
                return HttpResponse(template.render(context, request)) 
    except:
        context = {
            'error_messages': ['Something went wrong during saving']
        }
        return HttpResponse(template.render(context, request))    
    else:
        context = {
            'info_messages': [fb_message]
        }
        return HttpResponse(template.render(context, request))

@login_required(login_url='/')
def delete_workout(request, workout_id):
    template = loader.get_template('workout/list.html')
    member = request.user
    today = datetime.now()    
    
    workout_to_delete = get_object_or_404(Workout, pk=workout_id)
    
    try:
        workout_to_delete.delete()
    except:
        context = {
            'error_messages': ['Unable to delete workout {}'.format(workout_id)],
            'number_of_workouts': member.workout_set.filter(performed_date__week=today.isocalendar()[1]).count(),
            'workout_list': member.workout_set.all().order_by('-performed_date')[:50]
        }
        return HttpResponse(template.render(context, request))
    
    member = request.user

    context = {
        'info_messages': ['Deleted workout {}'.format(workout_id)],
        'number_of_workouts': member.workout_set.filter(performed_date__week=today.isocalendar()[1]).count(),
        'workout_list': member.workout_set.all().order_by('-performed_date')[:50]
    }
    return HttpResponse(template.render(context, request))


