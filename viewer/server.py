from flask import Flask, render_template, request, redirect, jsonify
import sys
sys.path.insert(0, '../src')
from src.race_manager import RaceManager

app = Flask(__name__)

# js = Bundle('brat/client/lib/head.load.min.js', 'process.js', output='gen/main.js')
# assets = Environment(app)
# assets.register('main_js', js)

RACE_MANAGER = RaceManager().load()


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html', races=RACE_MANAGER.races)


@app.route('/race-detail', methods=['GET'])
def post_home():
    race_name = request.args.get('races')
    race = RACE_MANAGER.races[race_name]
    return render_template('race.html', race=race)
