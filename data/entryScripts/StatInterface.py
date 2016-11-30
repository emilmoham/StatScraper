import django
django.setup()
from data.models import Team, Player, GameStats, SeasonStats

"""
These are just here to make me feel nice
gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']
"""

def getPerGameStat(team, playerName, statLabel):
	try:
		t = Team.objects.get(name=team)
	except Team.DoesNotExist:
		print("Team does not exist...")
		return None

	try:
		p = t.player_set.get(name=playerName)
	except Player.DoesNotExist:
		print("Player not found on specified team...")
		return None

	g = p.gamestats_set.get(player=p.id)
	
	try:
		return {
			'GP' : g.GamesPlayed,
			'MIN' : g.MinutesPlayed,
			'PPG' : g.Points,
			'RPG' : g.Rebounds,
			'APG' : g.Assists,
			'SPG' : g.Steals,
			'BPG' : g.Blocks,
			'TPG' : g.Turnovers,
			'FG%' : g.FieldGoalPercentage,
			'FT%' : g.FreeThrowPercentage,
			'3P%' : g.ThreePointPercentage,
		}[statLabel]
	except KeyError:
		print("No such statistic label")
		return None
