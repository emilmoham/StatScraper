import espnScraper
import django
django.setup()
from data.models import Team, Player, GameStats, SeasonStats
from django.utils import timezone

"""
These are just here to make me feel nice
gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']
"""

def insertPerGameStats(teamName):
	"""
	Scrapes per game statistics from ESPN about the team specified by teamName
	inserts gathered data into database if it does not already exist
	"""
	conflictCount = 0
	insertionCount = 0
	
	link = espnScraper.findTeamLink(teamName)
	dictionary = espnScraper.scrapePlayerData(link, 0)
	
	t = Team.objects.get(name=teamName)
	
	
	for player in dictionary:
		try:
			p = t.player_set.get(name=player['NAME'])
			#conflictCount = conflictCount + 1
		except Player.DoesNotExist:
			p = t.player_set.create(name=player['NAME'], last_updated=timezone.now())
			#insertionCount = insertionCount + 1
	
		try:
			p.gamestats_set.get(player=p.id)
			print("Skipping game stat insert for " + p.name)
			conflictCount = conflictCount + 1
		except GameStats.DoesNotExist:
			p.gamestats_set.create(GamesPlayed=player['GP'], MinutesPlayed=player['MIN'], Points=player['PPG'], Rebounds=player['RPG'], Assists=player['APG'], Steals=player['SPG'], Blocks=player['BPG'], Turnovers=player['TPG'], FieldGoalPercentage=player['FG%'], FreeThrowPercentage=player['FT%'], ThreePointPercentage=player['3P%'])
			insertionCount = insertionCount + 1

	print("Inserting Per Game Statistics for " + teamName + " Completed")
	print(" " + str(insertionCount) + "\tInsertions")
	print(" " + str(conflictCount) + "\tConflicts")


def insertSeasonTotalStats(teamName):
	"""
	Scrapes Season Total Statistics form ESPN about the team specified by teamName
	inserts gathered data into database if it does not already exist
	"""
	conflictCount = 0
	insertionCount = 0
	
	link = espnScraper.findTeamLink(teamName)
	ssdict = espnScraper.scrapePlayerData(link, 1)

	t = Team.objects.get(name=teamName)
	for player in ssdict:
		try:
			p = t.player_set.get(name=player['NAME'])
			#conflictCount = conflictCount + 1
		except Player.DoesNotExist:
			p = t.player_set.create(name=player['NAME'], last_update=Timezone.now())
			#insertionCount = insertionCount + 1
		try:
			p.seasonstats_set.get(player=p.id)
			print("Skipping seasonal stat insert for " + p.name)
			conflictCount = conflictCount + 1
		except SeasonStats.DoesNotExist:
			p.seasonstats_set.create(MinutesPlayed=player['MIN'], FieldGoalsMade=player['FGM'], FieldGoalsAttempted=player['FGA'], FreeThrowsMade=player['FTM'], FreeThrowsAttempted=player['FTA'], ThreePointsMade=player['3PM'], ThreePointsAttempted=player['3PA'], Points=player['PTS'], OffensiveRebounds=player['OFFR'], DefensiveRebounds=player['DEFR'], Rebounds=player['REB'], Assists=player['AST'], Turnovers=player['TO'], Steals=player['STL'], Blocks=player['BLK'])
			insertionCount = insertionCount + 1

	print("Inserting Season Total Statistics for " + teamName + " Completed")
	print(" " + str(insertionCount) + "\tInsertions")
	print(" " + str(conflictCount) + "\tConflicts")
