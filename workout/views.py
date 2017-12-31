from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django_facebook.api import get_persistent_graph

from .models import ActivityType, Workout

from datetime import date, datetime

import logging
log = logging.getLogger(__name__)

def get_activityTypes():
    return ActivityType.objects.all().exclude(name__contains='activity')

def get_workouts():
    return Workout.objects.all()

def list_workouts(request):
    today = datetime.now()
    member = request.user
    
    template = loader.get_template('workout/list.html')
    context = {
        'number_of_workouts': member.workout_set.filter(performed_date__week=today.isocalendar()[1]).count(),
        'workout_list': member.workout_set.all().order_by('-performed_date')[:30]
    }
    return HttpResponse(template.render(context, request))


# Create your views here.
def add_workout(request):
    """
    """
    try:
        log.error("Received add workout form {}".format(request.POST['performed_date']))
        template = loader.get_template('treningsveggen/index.html')
        graph = get_persistent_graph(request)
        fb_group_id = settings.TRENINGSVEGGEN_FB_GROUP_ID
        
        activity_type = ActivityType.objects.get(pk=request.POST['activity_type'])
        performed_date = request.POST['performed_date'].split('-')
        comment = request.POST['comment']
        performed = date(int(performed_date[0]), int(performed_date[1]), int(performed_date[2]))
        registered = date.today()
        
        newWorkout = Workout(member=request.user, performed_date=performed, registered_date=registered, primary_type=activity_type, comment=comment)
        newWorkout.save()
        
        fb_message = '{}. {} - {}'.format(newWorkout.number_in_week(), str(newWorkout), newWorkout.comment)
        graph.set('/{}/feed'.format(fb_group_id), {"message":fb_message})
        
    except:
        context = {
                    'activity_types': get_activityTypes(),
                    'error_messages': ['Something went wrong during saving']
                }
        return HttpResponse(template.render(context, request))    
    else:
        context = {
            'activity_types': get_activityTypes(),
            'info_messages': [fb_message]
        }
        return HttpResponse(template.render(context, request))

