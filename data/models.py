from django.db import models
from django.utils import timezone
class Conference(models.Model):
	name = models.CharField(max_length=100)
	
	@classmethod
	def create(cls, name):
		c = cls(name=name)
		c.save()
		return c

	def __str__(self):
		return self.name

class Team(models.Model):
	name = models.CharField(max_length=100)
	conference = models.ForeignKey(Conference, on_delete=models.CASCADE, null=True, default=None)
	pub_date = models.DateTimeField('date published')

	@classmethod
	def create(cls, name, conference):
		t = cls(name=name, conference=conference, pub_date=timezone.now())
		t.save()
		return t
	
	def __str__(self):
		return self.name

class Player(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	last_updated = models.DateTimeField('date published', default=None)

	def __str__(self):
		return (self.name)

class GameStats(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
	GamesPlayed = models.DecimalField(decimal_places=1, max_digits=3)
	MinutesPlayed = models.DecimalField(decimal_places=1, max_digits=3)
	Points = models.DecimalField(decimal_places=1, max_digits=3)
	Rebounds = models.DecimalField(decimal_places=1, max_digits=3)
	Assists = models.DecimalField(decimal_places=1, max_digits=3)
	Steals = models.DecimalField(decimal_places=1, max_digits=3)
	Blocks = models.DecimalField(decimal_places=1, max_digits=3)
	Turnovers = models.DecimalField(decimal_places=1, max_digits=3)
	FieldGoalPercentage = models.DecimalField(decimal_places=3, max_digits=4)
	FreeThrowPercentage = models.DecimalField(decimal_places=3, max_digits=4)
	ThreePointPercentage = models.DecimalField(decimal_places=3, max_digits=4)

	@classmethod
	def create(cls, GP, MIN, PPG, RPG, APG, SPG, BPG, TPG, FG, FT, TP):
		gamestats = cls(GamesPlayed=GP, MinutesPlayed=MIN, Points=PPG, Rebounds=RPG, Assists=APG, Steals=SPG, Blocks=BPG, Turnovers=TPG, FieldGoalPercentage=FG, FreeThrowPercentage=FT, ThreePointPercentage=TP)
		gamestats.save()
		return gamestats

	def __str__(self):
		return (self.player.__str__())

class SeasonStats(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
	MinutesPlayed = models.PositiveSmallIntegerField() #max value 32767
	FieldGoalsMade = models.PositiveSmallIntegerField() 
	FieldGoalsAttempted = models.PositiveSmallIntegerField() 
	FreeThrowsMade = models.PositiveSmallIntegerField() 
	FreeThrowsAttempted = models.PositiveSmallIntegerField() 
	ThreePointsMade = models.PositiveSmallIntegerField() 
	ThreePointsAttempted = models.PositiveSmallIntegerField() 
	Points = models.PositiveSmallIntegerField() 
	OffensiveRebounds = models.PositiveSmallIntegerField() 
	DefensiveRebounds = models.PositiveSmallIntegerField() 
	Rebounds = models.PositiveSmallIntegerField() 
	Assists = models.PositiveSmallIntegerField() 
	Turnovers = models.PositiveSmallIntegerField() 
	Steals = models.PositiveSmallIntegerField() 
	Blocks = models.PositiveSmallIntegerField()
	
	@classmethod
	def create(cls, MIN, FGM, FGA, FTM, FTA, TPM, TPA, PTS, OFFR, DEFR, REB, AST, TO, STL, BLK):
		seasonstats = cls(MinutesPlayed=MIN, FieldGoalsMade=FGM, FieldGoalsAttemted=FGA, FreeThrowsMade=FTM, FreeThrowsAttemted=FTA, ThreePointsMade=TPM, ThreePointsAttempted=TPA, Points=PTS, OffensiveRebounds=OFFR, DefensiveRebounds=DEFR, Rebounds=REB, Assists=AST, Turnovers=TO, Steals=STL, Blocks=BLK)
		seasonstats.save()
		return seasonStats
	
	def __str__(self):
		return (self.player.__str__())
