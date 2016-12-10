import django
django.setup()
from data.models import Conference, Team, Player, GameStats, SeasonStats

gameStatsLabels =  ["NAME", "GP", "MIN", "PPG", "RPG", "APG", "SPG", "BPG", "TPG", "FG%", "FT%", "3P%"]
seasonStatsLabels = ["NAME", "MIN", "FGM", "FGA", "FTM", "FTA", "3PM", "3PA", "PTS", "OFFR", "DEFR", "REB", "AST", "TO", "STL", "BLK"]

def getConfList():
	ret = []
	itr = 0
	c = Conference.objects.all()
	for conf in c:
		ret.insert(itr, conf.name)
		itr += 1
	return ret

def getTeamList(conference):
	try:
		c = Conference.objects.get(name=conference)
	except Conference.DoesNotExist:
		return None
	t = c.team_set.all()
	ret = []
	itr = 0
	for team in t:
		ret.insert(itr, team.name)
		itr += 1
	return ret

def getTeam(team, table):
	"""
	returns an object containing all players and their respective statistics
	statistics taken from table specified by <table>
	for team specified by <team>
	"""
	if table != "game" and table != "season":
		print("Invalid table specified")
		return None

	try:
		t = Team.objects.get(name=team)
	except Team.DoesNotExist:
		print("Team not found in database")
		return None
	
	p_set = t.player_set.all()
	p_count = 0
	ret = []
	for p in p_set:
		p_stats = {}
		p_stats["NAME"] = p.name
		if table == "game":
			g = p.gamestats_set.get(player=p.id)
			p_stats["GP"] = float(g.GamesPlayed)
			p_stats["MIN"] = float(g.MinutesPlayed)
			p_stats["PPG"] = float(g.Points)
			p_stats["RPG"] = float(g.Rebounds)
			p_stats["APG"] = float(g.Assists)
			p_stats["SPG"] = float(g.Steals)
			p_stats["BPG"] = float(g.Blocks)
			p_stats["TPG"] = float(g.Turnovers)
			p_stats["FG%"] = float(g.FieldGoalPercentage)
			p_stats["FT%"] = float(g.FreeThrowPercentage)
			p_stats["3P%"] = float(g.ThreePointPercentage)
		else:
			s = p.seasonstats_set.get(player=p.id)
			p_stats["MIN"] = s.MinutesPlayed
			p_stats["FGM"] = s.FieldGoalsMade
			p_stats["FGA"] = s.FieldGoalsAttempted
			p_stats["FTM"] = s.FreeThrowsMade
			p_stats["FTA"] = s.FreeThrowsAttempted
			p_stats["3PM"] = s.ThreePointsMade
			p_stats["3PA"] = s.ThreePointsAttempted
			p_stats["PTS"] = s.Points
			p_stats["OFFR"] = s.OffensiveRebounds
			p_stats["DEFR"] = s.DefensiveRebounds
			p_stats["REB"] = s.Rebounds
			p_stats["AST"] = s.Assists
			p_stats["TO"] = s.Turnovers
			p_stats["STL"] = s.Steals
			p_stats["BLK"] = s.Blocks
		ret.insert(p_count, p_stats)
	return ret

def getPlayer(team, playerName, table):
	"""
	returns an object containing
	all statistics in table specified by <table>
	Player specified by <player name>
	on team sepcified by <team>
	"""
	if table != "game" and table != "season":
		print("Invalid table specified")
		return None
	try:
		t = Team.objects.get(name=team)
	except Team.DoesNotExist:
		print("Team not found in database")
		return None

	try:
		p = t.player_set.get(name=playerName)
	except Player.DoesNotExist:
		print("Player not found on specified team")
		return None

	#There's probably a better way to do this but I'm strapped for time so whatever
	ret = {}
	if table == "game":
		g = p.gamestats_set.get(player=p.id)
		ret["GP"] = g.GamesPlayed
		ret["MIN"] = g.MinutesPlayed
		ret["PPG"] = g.Points
		ret["RPG"] = g.Rebounds
		ret["APG"] = g.Assists
		ret["SPG"] = g.Steals
		ret["BPG"] = g.Blocks
		ret["TPG"] = g.Turnovers
		ret["FG%"] = g.FieldGoalPercentage
		ret["FT%"] = g.FreeThrowPercentage
		ret["3P%"] = g.ThreePointPercentage
	else:
		s = p.seasonstats_set.get(player=p.id)
		ret["MIN"] = s.MinutesPlayed
		ret["FGM"] = s.FieldGoalsMade
		ret["FGA"] = s.FieldGoalsAttempted
		ret["FTM"] = s.FreeThrowsMade
		ret["FTA"] = s.FreeThrowsAttempted
		ret["3PM"] = s.ThreePointsMade
		ret["3PA"] = s.ThreePointsAttempted
		ret["PTS"] = s.Points
		ret["OFFR"] = s.OffensiveRebounds
		ret["DEFR"] = s.DefensiveRebounds
		ret["REB"] = s.Rebounds
		ret["AST"] = s.Assists
		ret["TO"] = s.Turnovers
		ret["STL"] = s.Steals
		ret["BLK"] = s.Blocks
	return ret

def getPerGameStat(team, playerName, statLabel):
	"""
	Returns the statistic in the GameStats table
	the statistic is  specified by <statLabel>
	for the player specified by <playerName>
	on the team specified by <teamName>
	"""
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
			"GP" : g.GamesPlayed,
			"MIN" : g.MinutesPlayed,
			"PPG" : g.Points,
			"RPG" : g.Rebounds,
			"APG" : g.Assists,
			"SPG" : g.Steals,
			"BPG" : g.Blocks,
			"TPG" : g.Turnovers,
			"FG%" : g.FieldGoalPercentage,
			"FT%" : g.FreeThrowPercentage,
			"3P%" : g.ThreePointPercentage,
		}[statLabel]
	except KeyError:
		print("No such statistic label")
		return None

def getSeasonTotalStat(team, playerName, statLabel):
	"""
	Returns the statistic in the SeasonStats table
	the statistic is  specified by <statLabel>
	for the player specified by <playerName>
	on the team specified by <teamName>
	"""
	try:
		t = Team.objects.get(name=team)
	except Team.DoesNotExist:
		print("Team does not exist")
		return None

	try:
		p = t.player_set.get(name=playerName)
	except Player.DoesNotExist:
		print("Specified player not found on team...")
		return None

	s = p.seasonstats_set.get(player=p.id)

	try:
		return {
			"MIN" : s.MinutesPlayed,
			"FGM" : s.FieldGoalsMade,
			"FGA" : s.FieldGoalsAttempted,
			"FTM" : s.FreeThrowsMade,
			"FTA" : s.FreeThrowsAttempted,
			"3PM" : s.ThreePointsMade,
			"3PA" : s.ThreePointsAttempted,
			"PTS" : s.Points,
			"OFFR" : s.OffensiveRebounds,
			"DEFR" : s.DefensiveRebounds,
			"REB" : s.Rebounds,
			"AST" : s.Assists,
			"TO" : s.Turnovers,
			"STL" : s.Steals,
			"BLK" : s.Blocks,
		}[statLabel]
	except KeyError:
		print("NO such statistic label")
		return None
