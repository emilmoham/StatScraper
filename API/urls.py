from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<team>\w+)/(?P<table>\w+)/$', views.get_team, name="get_team"),
]
