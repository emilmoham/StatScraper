import espnScraper

x = espnScraper.scrapePlayerData(espnScraper.findTeamLink("Temple"), 1)

for player in x:
	print(player)
	
