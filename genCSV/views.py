import io
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from data import StatInterface

gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']


def list_csv(request):
    context = {}
    return render(request, 'genCSV/landing.html', context)

def get_csv_by_conf(request):
    conf_list = StatInterface.getConfList()
    context = {
        "conf_list" : conf_list,
    }
    return render(request, 'genCSV/conf.html', context)

def down_by_conf(request):
    statTable = request.POST['stat_table']
    conf = request.POST['conf']
    conf = conf.replace('_', ' ')

    if statTable == 'game':
        labels = gameStatsLabels
    elif statTable == 'season':
        labels = seasonStatsLabels
    else:
        labels = None
    
    down = io.StringIO()

    down.write('Conference,')
    down.write('Team,')
    for stat in labels:
        if stat != 'NAME':
            down.write(',')
        down.write(stat)
    down.write('\n')


    team_set = StatInterface.getTeamList(conf)
    for team in team_set:
        player_set = StatInterface.getTeam(team, statTable)
        for player in player_set:
            down.write(conf)
            down.write(',')
            down.write(team)
            down.write(',')
            for stat in labels:
                if stat != 'NAME':
                    down.write(',')
                down.write(str(player[stat]))
            down.write('\n')

    response = HttpResponse(down.getvalue(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=conf.csv'
    return response

def get_csv_by_team(request):
    conf_list = StatInterface.getConfList()
    conf = request.GET.get('conf')
    team_set = None

    if conf != None:
        conf = conf.replace('_',' ')
        team_set = StatInterface.getTeamList(conf)
   
    context = {
        "conf_list" : conf_list,
        "conf" : conf,
        "team_set" : team_set,
    }
    return render(request, 'genCSV/team.html', context)

def down_by_team(request):
    conf = request.POST['conf']
    team = request.POST['team']
    statTable = request.POST['statType']
    
    team = unscrub(team)
    
    if statTable == 'game':
        labels = gameStatsLabels
    elif statTable == 'season':
        labels = seasonStatsLabels
    else:
        labels = None

    player_set = StatInterface.getTeam(team, statTable)
    if player_set == None:
        return none

    _file = io.StringIO()
    _file.write('Conference,')
    _file.write('Team,')
    for stat in labels:
        if stat != 'NAME':
            _file.write(',')
        _file.write(stat)
    _file.write('\n')

    for player in player_set:
        _file.write(conf)
        _file.write(',')
        _file.write(team)
        _file.write(',')
        for stat in labels:
            if stat != 'NAME':
                _file.write(',')
            _file.write(str(player[stat]))
        _file.write('\n')
    response = HttpResponse(_file.getvalue(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=team.csv'
    return response

def unscrub(value):
    value = value.replace('9', ';')
    value = value.replace('8', '&')
    value = value.replace('7', '(')
    value = value.replace('6', ')')
    value = value.replace('_', ' ')
    value = value.replace('5', '\'')
    return value;
