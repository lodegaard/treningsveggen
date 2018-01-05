from django import template

from workout.views import get_activityTypes

register = template.Library()

@register.simple_tag
def get_all_activities():
    return get_activityTypes()