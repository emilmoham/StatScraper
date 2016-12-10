import shutil
import io
from data import StatInterface

gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']


def create_full_csv(statTable):
    c_set = StatInterface.getConfList()
    _file = io.StringIO()

    #Checking our arguments
    if statTable == 'game':
        labels = gameStatsLabels
    elif statTable == 'season':
        labels = seasonStatsLabels
    else:
        return None

    for stat in labels:
        if(stat != 'NAME'):
            _file.write(',')
        _file.write(stat)
    _file.write('\n')

    for conf in c_set:
        t_set = StatInterface.getTeamList(conf)
        for team in t_set:
            player_set = StatInterface.getTeam(team, statTable)
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

    fd = open('full.csv', 'w')
    _file.seek(0)
    shutil.copyfileobj(_file, fd)
    fd.close()


create_full_csv('season')
