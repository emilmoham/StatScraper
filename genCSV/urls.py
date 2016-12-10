from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.list_csv , name="list_files"),
    url(r'^conf/$', views.get_csv_by_conf, name="select_by_conf"),
    url(r'^conf/dbc/$', views.down_by_conf, name="gen_by_conf"),
    url(r'^team/$', views.get_csv_by_team, name="select_by_team"),
    url(r'^team/dbt/$', views.down_by_team, name="gen_by_team"),
]
