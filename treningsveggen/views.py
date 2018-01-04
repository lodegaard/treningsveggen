from datetime import datetime
from math import ceil

from django.http import HttpResponse
from django.template import loader
from django_facebook.api import get_persistent_graph
from django_facebook.views import connect

from member.models import FacebookMember
from member.exceptions import IllegalUserException
from workout.views import get_activityTypes

import logging
log = logging.getLogger(__name__)

def translate_month_to_nor(month):
    return {
        1: 'Januar',
        2: 'Februar',
        3: 'Mars',
        4: 'April',
        5: 'Mai',
        6: 'Juni',
        7: 'Juli',
        8: 'August',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Desember'
    }.get(month)

def index(request):
    today = datetime.now()
    template = loader.get_template('treningsveggen/index.html')
    members = FacebookMember.objects.all()
    
    workouts = {}
    for member in members:
        workouts[member.first_name] = member.workout_set.filter(performed_date__year=today.year, performed_date__month=today.month).count()
    
    if not workouts.values():
        tally_scale = 0
    else:
        tally_scale = (ceil(max(workouts.values())/6)*2)/10
        
    
    context = {
        'activity_types': get_activityTypes(),
        'nor_month': translate_month_to_nor(today.month),
        'workouts': workouts,
        'tally_scale': tally_scale,
#        'fb_info': fb_info,
#        'members': group_members['data'][0]['id']
    }
    return HttpResponse(template.render(context, request))
    
    
    
def login(request):
    """
    Hack to control what users are allowed to register
    Since django_facebook doesn't have a method of handle 
    aborting of user registration, the call is wrapped so we can handle
    the exception raised by registration_backend
    """
    try:
        response = connect(request)
        return response
    except IllegalUserException:
        template = loader.get_template('treningsveggen/index.html')
        context = {
            'error_messages': ['Du er ikke medlem av treningveggen']
        }
        return HttpResponse(template.render(context, request))
    
    
    
    
    
    
