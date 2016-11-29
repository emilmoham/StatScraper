from django.db import models
from django.utils import timezone

class Team(models.Model):
	name = models.CharField(max_length=100)
	pub_date = models.DateTimeField('date published')

	@classmethod
	def create(cls, name):
		team = cls(name=name, pub_date = timezone.now())
		team.save()
		return team
	
	def __str__(self):
		return self.name

class Player(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	firstName = models.CharField(max_length=100)
	lastName = models.CharField(max_length=100)
	last_updated = models.DateTimeField('date published', default=None)

	@classmethod
	def create(cls, firstName, lastName, team):
		p = cls(team=Team, firstName=firstName, lastName=lastName, last_updated=timezone.now())
		return p

	def __str__(self):
		return (self.firstName + " " + self.lastName)

