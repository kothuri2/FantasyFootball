from pymongo import MongoClient
import unittest

class MongoTest(unittest.TestCase):
	def test_teams(self):
		client = MongoClient('localhost:27017')
		nfl_db = client['nfl-team']
		steelers = nfl_db.all_team.find_one({'name': 'Pittsburgh Steelers'})
		self.assertEquals('Pittsburgh Steelers', steelers['name'])
		self.assertEquals('AFC North', steelers['division'])

	def test_players(self):
		client = MongoClient('localhost:27017')
		nfl_db = client['nfl-team']
		player_name = 'Ben Roethlisberger'
		cursor = nfl_db.all_team.find_one({'players.name': player_name})
		for player in cursor['players']:
			if(player['name'] == player_name):
				self.assertEquals('Ben Roethlisberger', player['name'])
				self.assertEquals('Miami (OH)', player['college'])

if __name__ == '__main__':
	unittest.main()