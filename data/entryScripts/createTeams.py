import django
django.setup();
from data.models import Team
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

insertionCount = 0
conflictCount = 0

conferences = soup.find_all(conferenceTag, {"class" : conferenceClass})
for conference in conferences:
	conferenceName = conference.find(conferenceNameTag).get_text()
	teams = conference.find_all(teamContainerTag)
	for team in teams:
		teamName = team.find(teamNameTag).get_text()
		teamSet = Team.objects.filter(name=teamName)
		if(len(teamSet) == 0):
			insertionCount = insertionCount + 1
			Team.create(teamName, conferenceName)
		else:
			conflictCount = conflictCount + 1
			print("Team <" + teamName + "> already in database")
			print("\tConflicts with: " + teamSet.__str__())
print("Operation completed.")
print(" " + str(insertionCount) + "\tInsertions")
print(" " + str(conflictCount) + "\tConflicts")

