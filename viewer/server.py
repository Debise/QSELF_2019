from flask import Flask, render_template, request, redirect, jsonify
import sys
import os
import glob
sys.path.insert(0, '../')
import settings as st
from src.race_manager import RaceManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# js = Bundle('brat/client/lib/head.load.min.js', 'process.js', output='gen/main.js')
# assets = Environment(app)
# assets.register('main_js', js)

RACE_MANAGER = RaceManager().load()


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html', races=RACE_MANAGER.races)


@app.route('/race-detail', methods=['POST'])
def post_race_detail():
    race_name = request.form['races']
    race = RACE_MANAGER.races[race_name]
    return render_template('race.html', race=race)


@app.route('/race-detail/visualisation', methods=['POST'])
def post_visualisation():
    race_name = request.form['race_name']
    output_folder = st.files["output_folder"]
    filename = os.path.join(output_folder, f"{race_name}.html")

    if filename not in glob.glob(f'{output_folder}/*.html'):
        RACE_MANAGER.races[race_name].draw()

    json_dict = {'filename': f"/static/output/{race_name}.html"}

    return jsonify(json_dict)


@app.route('/race-detail/statistics', methods=['POST'])
def post_statistic():
    race_name = request.form['race_name']
    json_dict = RACE_MANAGER.races[race_name].get_statistics()

    return jsonify(json_dict)


if __name__ == '__main__':
    app.run()
