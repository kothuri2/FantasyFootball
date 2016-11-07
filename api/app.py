from flask import Flask
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'nfl-team'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/nfl-team'

mongo = PyMongo(app)

@app.route("/get_team/<team_name>")
def get_team(team_name):
	cursor = mongo.db.all_team.find_one({'name': team_name})
	if(cursor is not None):
		del cursor['players']
		return dumps(cursor)
	return jsonify({'result': 'Team Not Found'})

@app.route("/get_player/<player_name>")
def get_player(player_name):
	cursor = mongo.db.all_team.find_one({'players.name': player_name})
	for player in cursor['players']:
		if(player['name'] == player_name):
			return jsonify({'result': player})
	return jsonify({'result': 'Player Not Found'})

if __name__ == '__main__':
	app.run(debug=True)