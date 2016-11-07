'''
Source: footballdb.com for all web scraping
'''
import urllib
from bs4 import BeautifulSoup
import json

base_url =  'http://www.footballdb.com/'
home_page = 'http://www.footballdb.com/teams/index.html'
home_page_read = urllib.urlopen(home_page).read()
soup = BeautifulSoup(home_page_read, "lxml")

def main():
	'''main method to call the helper functions and scrape the information needed'''
	nfl_teams_dict = scrape_teams_info()
	i = 1
	for division in nfl_teams_dict:
		for team in nfl_teams_dict[division]:
			print(team['name'], i)
			scrape_player_info(team)
			i += 1
	with open('teams.json', 'w') as fp:
		json.dump(nfl_teams_dict, fp, indent=4)

def scrape_teams_info():
	'''Scrape all teams and their corresponding links on footballdb.com'''
	nfl_teams_dict = {}
	teams_table = soup.find("table", class_="statistics")
	teams = teams_table.find_all("tr")
	current_divison = ''
	for team in teams:
		if(team.has_attr('class') and team['class'][0] == 'header'):
			current_divison = team.text.strip()
			nfl_teams_dict[team.text.strip()] = []
		else:
			team_info = team.find_all('td')
			team_name = team_info[0].text.strip()
			team_links = team_info[1].find_all('a')
			new_team = {
				'name': team_name.encode('utf-8'),
				'roster_link': base_url + team_links[0]['href'],
				'stats_link': base_url + team_links[1]['href'],
				'schedule_link': base_url + team_links[2]['href'],
				'draft_link': base_url + team_links[3]['href'],
				'transactions_link': base_url + team_links[4]['href'],
				'history_link': base_url + team_links[5]['href']
			}
			scrape_team_schedule(new_team)
			nfl_teams_dict[current_divison].append(new_team)
	return nfl_teams_dict

def scrape_team_schedule(new_team):
	new_team['schedule'] = []
	new_team_read = urllib.urlopen(new_team['schedule_link']).read()
	new_team_soup = BeautifulSoup(new_team_read, "lxml")

	reg_season_table = new_team_soup.find("table", class_='statistics')
	reg_season_table_headers = reg_season_table.find('thead').find('tr').find_all('td')
	col_values = reg_season_table.find('tbody').find_all('tr')
	reg_season_table_headers_text = []
	for header in reg_season_table_headers:
		reg_season_table_headers_text.append(header.text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip())
	for value in col_values:
		values = value.find_all('td')
		game = {}
		for i in range(len(values)):
			game[reg_season_table_headers_text[i]] = values[i].text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip()
		new_team['schedule'].append(game)
	del new_team['schedule_link']


def scrape_player_info(team):
	'''Scrape player info by team and append to team info for each team'''
	roster_link = team['roster_link']
	roster_read = urllib.urlopen(roster_link).read()
	roster_soup = BeautifulSoup(roster_read, "lxml")
	players_table = roster_soup.find("table", class_="statistics")
	players = (players_table.find('tbody')).find_all('tr')
	for player in players:
		player_info = player.find_all('td')

		#Reformat strings
		number = player_info[0].text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip()
		name = player_info[1].text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip()
		birthdate = player_info[5].text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip()
		college = player_info[6].text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip()

		new_player = {
			'number': number,
			'name': name,
			'player_link': base_url + player_info[1].find('a')['href'],
			'birthdate': birthdate,
			'college': college
		}
		player_img__read = urllib.urlopen(new_player['player_link']).read()
		player_img_soup = BeautifulSoup(player_img__read, "lxml")

		#scrape player stats
		scrape_player_stats(new_player)

		try:
			new_player['player_img'] = player_img_soup.find(id='playerimg')['src']
		except:
			new_player['player_img'] = None
		if 'players' not in team:
			team['players'] = [new_player]
		else:
			team['players'].append(new_player)

def scrape_player_stats(new_player):
	'''Scrape the individual career stats of each player'''
	player_stats_read = urllib.urlopen(new_player['player_link'] + '/stats').read()
	player_stats_soup = BeautifulSoup(player_stats_read, "lxml")

	player_stats_labels = player_stats_soup.find_all('div', class_='divider')
	player_stats_tables = player_stats_soup.find_all('table', class_='statistics')
	if(len(player_stats_labels) != len(player_stats_tables)):
		print('Something is seriously wrong here')
	
	for label, table in zip(player_stats_labels, player_stats_tables):
		table_label = label.find('h2').text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip()
		new_player[table_label] = []
		#Get all the column headers
		col_headers = table.find('thead').find_all('tr')
		if(len(col_headers) > 1):
			col_headers = col_headers[1].find_all('th')
		elif(len(col_headers) == 1):
			col_headers = col_headers[0].find_all('th')
		col_headers_text = []
		#Get all the column headers in text form
		for header in col_headers:
			col_headers_text.append(header.text.encode('utf-8').replace('\xc2\xa0', ' ').rstrip())
		#Get all the column values
		column_values = table.find('tbody').find_all('tr')
		for col_val in column_values:
			values = col_val.find_all('td')
			yearly_stats = {}
			for i in range(len(values)):
				yearly_stats[col_headers_text[i]] = values[i].text
			new_player[table_label].append(yearly_stats)
main()
