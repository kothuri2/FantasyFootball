import unittest
import json

'''
Scraper Test class that reads in the json file outputted by the scraper
and tests that valid information exists inside
'''
class ScraperTest(unittest.TestCase):
	def test_divisions(self):
		team_json = json.loads(open('/Users/Radhir/College/Junior/CS242/FantasyFootball/teams.json').read())

		self.assertEquals(True, 'AFC North' in team_json)
		self.assertEquals(True, 'AFC East' in team_json)
		self.assertEquals(True, 'AFC South' in team_json)
		self.assertEquals(True, 'AFC West' in team_json)
		self.assertEquals(True, 'NFC North' in team_json)
		self.assertEquals(True, 'NFC East' in team_json)
		self.assertEquals(True, 'NFC South' in team_json)
		self.assertEquals(True, 'NFC West' in team_json)

	def test_teams(self):
		team_json = json.loads(open('/Users/Radhir/College/Junior/CS242/FantasyFootball/teams.json').read())
		afc_north_teams = team_json['AFC North']
		afc_north_names = []
		for team in afc_north_teams:
			afc_north_names.append(team['name'])
		self.assertEquals(True, 'Pittsburgh Steelers' in afc_north_names)
		self.assertEquals(True, 'Baltimore Ravens' in afc_north_names)
		self.assertEquals(True, 'Cleveland Browns' in afc_north_names)
		self.assertEquals(True, 'Cincinnati Bengals' in afc_north_names)

		afc_south_teams = team_json['AFC South']
		afc_south_names = []
		for team in afc_south_teams:
			afc_south_names.append(team['name'])
		self.assertEquals(True, 'Indianapolis Colts' in afc_south_names)
		self.assertEquals(True, 'Houston Texans' in afc_south_names)
		self.assertEquals(True, 'Jacksonville Jaguars' in afc_south_names)
		self.assertEquals(True, 'Tennessee Titans' in afc_south_names)

		#NFC
		nfc_north_teams = team_json['NFC North']
		nfc_north_names = []
		for team in nfc_north_teams:
			nfc_north_names.append(team['name'])
		self.assertEquals(True, 'Green Bay Packers' in nfc_north_names)
		self.assertEquals(True, 'Chicago Bears' in nfc_north_names)
		self.assertEquals(True, 'Minnesota Vikings' in nfc_north_names)
		self.assertEquals(True, 'Detroit Lions' in nfc_north_names)

		nfc_south_teams = team_json['NFC South']
		nfc_south_names = []
		for team in nfc_south_teams:
			nfc_south_names.append(team['name'])
		self.assertEquals(True, 'Atlanta Falcons' in nfc_south_names)
		self.assertEquals(True, 'New Orleans Saints' in nfc_south_names)
		self.assertEquals(True, 'Tampa Bay Buccaneers' in nfc_south_names)
		self.assertEquals(True, 'Carolina Panthers' in nfc_south_names)

	def test_schedules(self):
		team_json = json.loads(open('/Users/Radhir/College/Junior/CS242/FantasyFootball/teams.json').read())
		#Steelers players
		schedule = team_json['AFC North'][3]['schedule']
		test_schedule = {
            "Date": "09/18/201609/18/16", 
            "Result": "W 24-16", 
            "Location": "Heinz Field (Pittsburgh, PA)", 
            "Attend": "65,072",
            "Opponent": "Cincinnati"
        }
		self.assertEquals(True, test_schedule in schedule)

	def test_players(self):
		team_json = json.loads(open('/Users/Radhir/College/Junior/CS242/FantasyFootball/teams.json').read())
		#Steelers players
		players = team_json['AFC North'][3]['players']
		players_names = []
		for player in players:
			players_names.append(player['name'])

		self.assertEquals(True, 'Ben Roethlisberger' in players_names)
		self.assertEquals(True, 'Antonio Brown' in players_names)
		self.assertEquals(True, 'Xavier Grimble' in players_names)
		self.assertEquals(True, 'Markus Wheaton' in players_names)

		

if __name__ == '__main__':
	unittest.main()

