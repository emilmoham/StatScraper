import espnScraper

x = espnScraper.scrapePlayerData(espnScraper.findTeamLink("Temple"))

for player in x:
	print(player)
	
