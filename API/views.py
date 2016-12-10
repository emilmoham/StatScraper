import io
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from data import StatInterface

gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']

def list_conferences(request):
    conf_list = StatInterface.getConfList()

    conf_dict = {}
    data = io.StringIO()
    data.write('[')
    for conf in conf_list:
        conf_dict[conf] = scrub(conf)
    data.write(str(json.dumps(conf_dict, sort_keys=True)))
    data.write(']')

    return_string = data.getvalue()
    return_string = return_string.replace(',', ',\n')

    return HttpResponse(return_string, content_type='text/plain')

def list_teams(request, conference=None):
    team_dict = {}
    if conference != None:
        team_list = StatInterface.getTeamList(unscrub(conference))
        if team_list == None:
            return HttpResponseNotFound('<h1>Conference does not exist.</h1>')
        for team in team_list:
            team_dict[team] = scrub(team)
    else:
        conf_list = StatInterface.getConfList()
        for conf in conf_list:
            team_list = StatInterface.getTeamList(conf)
            for team in team_list:
                team_dict[team] = scrub(team)

    data = io.StringIO()
    data.write('[')
    data.write(str(json.dumps(team_dict, sort_keys=True)))
    data.write(']')
    return_string = data.getvalue()
    return_string = return_string.replace(',',',\n')

    return HttpResponse(return_string, content_type="text/plain")
        

def get_team(request, team, table):
    team = unscrub(team)
    if table == 'game':
        labels = gameStatsLabels
    elif table  == 'season':
        lables = seasonStatsLabels
    else:
        return HttpResponseNotFound('<h1>Invalid table specified.</h1>')

    team_obj = StatInterface.getTeam(team, table)
    if team_obj == None:
        return HttpResponseNotFound('<h1>Team does not exist in database</h1>')
    count = 0
    data = io.StringIO()
    data.write('[')
    for player in team_obj:
        data.write(str(json.dumps(player)))
        if count < (len(team_obj) - 1):
            count += 1
            data.write(',\n')
    data.write(']')

    response = HttpResponse(data.getvalue(), content_type='text/plain')
    return response
    
def scrub(value):
    value = value.replace(';','9')
    value = value.replace('&','8')
    value = value.replace('(','7')
    value = value.replace(')','6')
    value = value.replace(' ','_')
    value = value.replace('\'','5')
    return value

def unscrub(value):
    value = value.replace('9', ';')
    value = value.replace('8', '&')
    value = value.replace('7', '(')
    value = value.replace('6', ')')
    value = value.replace('_', ' ')
    value = value.replace('5', '\'')
    return value;
