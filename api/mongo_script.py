'''
Script that is used to read from teams.json
and push all teams into database
'''

from pymongo import MongoClient
import json

#production client
#client = MongoClient('mongodb://kothuri2:HelloThere!@ds143717.mlab.com:43717/nfl-team')

#local client
client = MongoClient('localhost:27017')

nfl_db = client['nfl-team']
team_json = json.loads(open('/Users/Radhir/College/Junior/CS242/FantasyFootball/teams.json').read())

for division in team_json:
	for team in team_json[division]:
		team['division'] = str(division)

for division in team_json:
	team_json[division]
	record_id = nfl_db.all_team.insert(team_json[division])