from django.shortcuts import render
from django.template import loader
from .models import Conference, Team, Player
from . import StatInterface

gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']


def select(request):
	conf_list = Conference.objects.all()
	conf1 = request.GET.get('c1')
	conf2 = request.GET.get('c2')
	team1_list = None
	team2_list = None
	team1_name = request.GET.get('t1')
	team2_name = request.GET.get('t2')
	stat_list = request.GET.get('statlist')
	
	if(conf1 != None and conf2 != None):
		for conf in conf_list:
			if conf.name.replace(' ','') == conf1:
				team1conf = conf
			if conf.name.replace(' ','') == conf2:
				team2conf = conf
		team1_list = team1conf.team_set.all()
		team2_list = team2conf.team_set.all()
	
	context = {
		"conf_list" : conf_list,
		"conf1" : conf1,
		"conf2" : conf2,
		"team1_list" : team1_list,
		"team2_list" : team2_list,
		"team1" : team1_name,
		"team2" : team2_name,
		"stat_list" : stat_list,
	}
	
	return render(request, 'data/select.html', context)

def compare(request, team1='', team2='', statType='game'):
	weights = None
	favored = None
	if statType == 'game':
		labels = gameStatsLabels
	elif statType == 'season':
		labels = seasonStatsLabels
	else:
		statType = 'game'
		invalidParam = True
		labels = game
	
	team1_obj = StatInterface.getTeam(team1, statType)
	team1_stat_totals = calcTotals(team1_obj, labels)
	team1_stat_weighted = {}
	team2_obj = StatInterface.getTeam(team2, statType)
	team2_stat_totals = calcTotals(team2_obj, labels)
	team2_stat_weighted = {}

	if team1_obj != None and team2_obj != None:
		#Get the user's weights
		weights = {}
		for label in labels:
			weights[label] = request.GET.get(label.replace('%','_'))
			if weights[label] == None:
				weights[label] = "0.0"

		#Applying the weights
		team1_total = 0
		team2_total = 0
		for label in labels:
			if label == 'NAME':
				continue
			team1_stat_weighted[label] = float(team1_stat_totals[label]) * float(weights[label])
			team1_total += team1_stat_weighted[label]
			team2_stat_weighted[label] = float(team2_stat_totals[label]) * float(weights[label])
			team2_total += team2_stat_weighted[label]

		if team1_total > team2_total:
			favored = team1
		elif team1_total < team2_total:
			favored = team2a
	#endif

	context = {
		"team1" : team1,
		"team2" : team2,
		"statType" : statType,
		"labels" : labels,
		"weights" : weights,
		"team1_obj" : team1_obj,
		"team1_totals" : team1_stat_totals,
		"team1_stat_weighted" : team1_stat_weighted,
		"team2_obj" : team2_obj,
		"team2_totals" : team2_stat_totals,
		"team2_stat_weighted" : team2_stat_weighted,
		"favored" : favored,
	}
	return render(request, 'data/compare.html', context)

def calcTotals(team_obj, labels):
	if team_obj == None:
		return None
	team_stat_totals = {}
	
	#initialize all values to zero
	for stat in labels:
		if stat == 'NAME':
			continue
		team_stat_totals[stat] = 0

	for player in team_obj:
		for stat in labels:
			if stat == 'NAME':
				continue
			team_stat_totals[stat] += player[stat]

	return team_stat_totals
