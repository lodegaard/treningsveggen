from datetime import datetime
from django import template
from math import ceil

from member.models import FacebookMember

register = template.Library()

@register.inclusion_tag('workout/tally_workouts.html')
def tally_workouts():
    today = datetime.now()
    members = FacebookMember.objects.all().order_by('first_name')
    
    workouts = {}
    for member in members:
        workouts[member.first_name] = member.workout_set.filter(performed_date__year=today.year, performed_date__month=today.month).count()
    
    return {
        'tally_workouts' : workouts,
    }
  
@register.simple_tag
def tally_scale():
    today = datetime.now()
    members = FacebookMember.objects.all()
    
    workouts = {}
    for member in members:
        workouts[member.first_name] = member.workout_set.filter(performed_date__year=today.year, performed_date__month=today.month).count()
    
    if not workouts.values():
        tally_scale = 0
    else:
        tally_scale = (ceil(max(workouts.values())/6)*2)/10
        
    return tally_scale

@register.simple_tag
def get_month():
    month = datetime.now().month
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