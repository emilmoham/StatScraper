import shutil
import io
import json
from data import StatInterface

team_obj = StatInterface.getTeam('Temple', 'season')

data = io.StringIO()
count = 0
for player in team_obj:
    data.write(str(json.dumps(player)))
    if count < len(team_obj)-1:
        count += 1;
        data.write('\n')
data.write(']')

fd = open('test.txt', 'w')
data.seek(0)
shutil.copyfileobj(data, fd)
fd.close()
