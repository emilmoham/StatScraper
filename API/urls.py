from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'conferences/$', views.list_conferences, name="list_conferences"),
    url(r'teams/$', views.list_teams, name="list_teams_none"),
    url(r'teams/(?P<conference>\w+)/$', views.list_teams, name="list_teams_conf"),
    url(r'(?P<team>\w+)/(?P<table>\w+)/$', views.get_team, name="get_team"),
]
