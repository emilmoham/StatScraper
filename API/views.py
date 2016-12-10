import io
import json
from django.http import HttpResponse
from django.shortcuts import render
from data import StatInterface

gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']

def get_team(request, team, table):
    team = unscrub(team)
    if table == 'game':
        labels = gameStatsLabels
    elif table  == 'season':
        lables = seasonStatsLabels
    else:
        return None

    team_obj = StatInterface.getTeam(team, table)
    count = 0
    data = io.StringIO()
    data.write('[')
    for player in team_obj:
        data.write(str(json.dumps(player)))
        if count < (len(team_obj) - 1):
            count += 1
            data.write(',')
    data.write(']')

    response = HttpResponse(data.getvalue(), content_type='text/plain')
    return response
    
        
def unscrub(value):
    value = value.replace('9', ';')
    value = value.replace('8', '&')
    value = value.replace('7', '(')
    value = value.replace('6', ')')
    value = value.replace('_', ' ')
    value = value.replace('5', '\'')
    return value;
