import sys
import requests
from bs4 import BeautifulSoup

#URLs
baseURL = "http://www.espn.com"
teamListingsURL = "/ncb/teams"

#Useful Tags
conferenceTag = "ul"
conferenceClass = "medium-logos"
teamContainerTag = "li"
teamNameTag = "h5"

tableTag = "table"
tableClass = "tablehead"
playerTag = "tr"
statTag = "td"

gameStatsLabels =  ['NAME', 'GP', 'MIN', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%']
seasonStatsLabels = ['NAME', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OFFR', 'DEFR', 'REB', 'AST', 'TO', 'STL', 'BLK']

def findTeamLink(teamName):
	"""
	returns a string containing the link to a team's statistics table on ESPN
	"""
	r = requests.get(baseURL + teamListingsURL)
	soup = BeautifulSoup(r.content, "html.parser")

	conferences = soup.find_all(conferenceTag, {"class" : conferenceClass})
	exit_flag = 0
	for conference in conferences:
		if(exit_flag == 1):
			break
		teams = conference.find_all(teamContainerTag)
		for team in teams:
			t = team
			if(team.find(teamNameTag).get_text() == teamName):
				exit_flag = 1
				break
	tLink = t.find_all('a')[1].get('href')
	return tLink

def scrapePlayerData(teamLink):
	"""
	returns an array of all players and their statistics for the team specified by teamLink
	"""
	r = requests.get(baseURL + teamLink)
	soup = BeautifulSoup(r.content, "html.parser")
	tables = soup.find_all(tableTag, {"class" : tableClass})
	players = tables[0].find_all(playerTag)
	skip = 0
	playerCount = 0
	retList = []
	for player in players:
		d = {}
		if(skip < 2 or  skip == len(players) - 1):
			#Skipping First two rows which are just titles
			skip = skip + 1
			continue
		skip = skip + 1
		iteration = 0
		information = player.find_all(statTag)
		for info in information:
			#Handling Names
			if(iteration < 1):
				iteration = iteration + 1
				Name = info.get_text()
				d['NAME'] = Name
				continue
			#Handling the rest of the statistics
			d[gameStatsLabels[iteration]] = float(info.get_text())
			iteration = iteration + 1
		retList.insert(playerCount, d)
		playerCount = playerCount + 1
	return retList
		
