import django
django.setup();
from django.utils import timezone
from data.models import Conference, Team
import requests
from bs4 import BeautifulSoup

#WebPage with all D1 Teams
baseURL = "http://www.espn.com/ncb/teams"

#Useful tags and classes
conferenceTag = "div"
conferenceClass = "mod-container mod-open-list mod-teams-list-medium mod-no-footer"
conferenceNameTag = "h4"
teamContainerTag = "li"
teamNameTag = "h5"

r = requests.get(baseURL)
soup = BeautifulSoup(r.content, "html.parser")

conferenceInsertionCount = 0
conferenceConflictCount = 0
teamInsertionCount = 0
teamConflictCount = 0

tables = soup.find_all(conferenceTag, {"class" : conferenceClass})
for table in tables:
	conferenceName = table.find(conferenceNameTag).get_text()
	try:
		c = Conference.objects.get(name=conferenceName)
		conferenceConflictCount = conferenceConflictCount + 1
	except Conference.DoesNotExist:
		c = Conference.create(conferenceName)
		conferenceInsetionCount = conferenceInsertionCount + 1

	teams = table.find_all(teamContainerTag)
	for team in teams:
		teamName = team.find(teamNameTag).get_text()
		teamSet = c.team_set.filter(name=teamName)
		if(len(teamSet) == 0):
			teamInsertionCount = teamInsertionCount + 1
			c.team_set.create(name=teamName, pub_date=timezone.now())
		else:
			teamConflictCount = teamConflictCount + 1
			print("Team <" + teamName + "> already in database")
			print("\tConflicts with: " + teamSet.__str__())
print("Operation completed.")
print(" " + str(conferenceInsertionCount) + "\tConference Entry Insertions")
print(" " + str(conferenceConflictCount) + "\tConference Entry Conflicts")
print(" " + str(teamInsertionCount) + "\tTeam Entry Insertions")
print(" " + str(teamConflictCount) + "\tTeam Entry Conflicts")

