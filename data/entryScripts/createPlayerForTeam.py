import sys
import django
django.setup()
from data.models import Team, Player, GameStats, SeasonStats
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

#Checking arguments
if(len(sys.argv) < 2):
	print("Usage: " + sys.argv[0] + " <Team Name>")
	exit()

try:
	t = Team.objects.get(name=sys.argv[1])
except Team.DoesNotExist:
	print("Error: Team does not exist in database")
	exit()

#insertionCount = 0
#conflictCount = 0

r = requests.get(baseURL + teamListingsURL)
soup = BeautifulSoup(r.content, "html.parser")

conferences = soup.find_all(conferenceTag, {"class" : conferenceClass})
exit_flag = 0
for conference in conferences:
	if(exit_flag == 1):
		break;
	teams = conference.find_all(teamContainerTag)
	for team in teams:
		t = team
		if(team.find(teamNameTag).get_text() == sys.argv[1]):
			exit_flag = 1
			break;

tLink = t.find_all('a')[1].get('href')

#Scraping Team Specific data
r = requests.get(baseURL + tLink)
soup = BeautifulSoup(r.content, "html.parser")

tables = soup.find_all(tableTag, {"class" : tableClass})
players = tables[0].find_all(playerTag)
skip = 0
ret = {}
for player in players:
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
			Name = Name.split()
			continue
		#Handling the rest of the statistics
		ret[iteration - 1] = float(info.get_text())
		iteration = iteration + 1
		g = GameStats.create(ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7], ret[8], ret[9], ret[10])
	print(Name)
