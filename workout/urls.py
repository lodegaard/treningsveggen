from django.conf.urls import url

from . import views

app_name = 'workout'
urlpatterns = [
    url(r'add/$', views.add_workout, name='add'),
    url(r'list/$', views.list_workouts, name='list'),
]