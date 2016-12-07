import insertionScripts
import django
django.setup()
from data.models import Team

t = Team.objects.all()
for i in range (0, len(t)):
	insertionScripts.insertPerGameStats(t[i].name)
	insertionScripts.insertSeasonTotalStats(t[i].name)
