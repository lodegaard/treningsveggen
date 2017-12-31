from datetime import datetime
from math import ceil

from django.http import HttpResponse
from django.template import loader

from django_facebook.api import get_persistent_graph

from member.models import FacebookMember
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
        
    context = {
        'activity_types': get_activityTypes(),
        'nor_month': translate_month_to_nor(today.month),
        'workouts': workouts,
        'tally_scale': (ceil(max(workouts.values())/6)*2)/10,
    }
    return HttpResponse(template.render(context, request))
    