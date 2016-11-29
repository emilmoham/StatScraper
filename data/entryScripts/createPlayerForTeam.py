import sys
import django
django.setup()
from data.models import Team, Player
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

print(tLink)
