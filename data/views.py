from django.shortcuts import render
from django.template import loader
from .models import Conference, Team, Player

def index(request):
	conf_list = Conference.objects.all()
	conf1 = request.GET.get('conference1')
	conf2 = request.GET.get('conference2')
	team1_list = None
	team2_list = None
	team1_name = request.GET.get('team1')
	team2_name = request.GET.get('team2')
	team1_player_set = None
	team2_player_set = None
	
	if(conf1 != None and conf2 != None):
		for conf in conf_list:
			if conf.name.replace(' ','') == conf1:
				team1conf = conf
			if conf.name.replace(' ','') == conf2:
				team2conf = conf
		team1_list = team1conf.team_set.all()
		team2_list = team2conf.team_set.all()

	if(team1_name != None and team2_name != None):
		for team in team1_list:
			if(team.name.replace(' ','') == team1_name):
				team1_player_set = team.player_set.all()
		for team in team2_list:
			if(team.name.replace(' ','') == team2_name):
				team2_player_set = team.player_set.all()
	
	context = {
		"conf_list" : conf_list,
		"conf1" : conf1,
		"conf2" : conf2,
		"team1_list" : team1_list,
		"team2_list" : team2_list,
		"team1" : team1_name,
		"team2" : team2_name,
		"team1_player_set" : team1_player_set,
		"team2_player_set" : team2_player_set,
	}
	
	return render(request, 'data/index.html', context)
