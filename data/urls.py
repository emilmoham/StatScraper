from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.select, name="select"),
	url(r'^(?P<team1>\w+)/(?P<team2>\w+)/(?P<statType>\w+)/$', views.compare, name="compare"),
]
