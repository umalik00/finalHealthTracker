from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^$', views.startup, name='startup'),
    re_path('^home/$', views.home, name='home'),
    re_path('^login/$', views.loginView, name='login'),
    re_path('^logout/$', views.logoutView, name='logout'),
    re_path('^register/$', views.registerView, name='register'),
    re_path('^goals/$', views.userGoals, name='goals'),
    re_path('^exercise/$', views.exercise, name='exercise'),
    re_path('^weightLift/$', views.recordWeightLift, name='weightLift'),
    re_path('^cardio/$', views.recordCardio, name='cardio'),
    re_path('^bodyWeight/$', views.recordBodyWeight, name='bodyWeight'),
    re_path('^meal/$', views.addMeal, name='meal'),
    re_path('^group/$', views.group, name='groups'),
    re_path('^createGroup/$', views.createGroup, name='createGroups'),
    re_path('^join/$', views.joinUserGroup, name='join'),
    re_path('^mealItems/$', views.mealItem, name='mealItem'),
    re_path('^group/(?P<groupID>[0-9]+)/$',views.joinedGroup, name='joinedGroup'),
]
