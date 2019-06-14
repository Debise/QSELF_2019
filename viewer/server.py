from flask import Flask, render_template, request, jsonify
import sys
import os
import glob
sys.path.insert(0, '../')
import settings as st
from src.race_manager import RaceManager
from src.race_inferer_wrapper import RaceInfererWrapper
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

RACE_MANAGER = RaceManager().load()
RACE_INFERER = RaceInfererWrapper()


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


@app.route('/race-detail/comparison_segments', methods=['POST'])
def get_comparison_segments():
    race_name = request.form['race_name']
    deniv_segment, length_segment, density_segment = RACE_INFERER.get_best_segment(race_name)
    segments = deniv_segment + length_segment + density_segment

    json_dict = {}

    for i, segment_tuple in enumerate(segments):
        second_race = segment_tuple[0]
        segment = segment_tuple[1]

        json_dict[f'seg{i}'] = [second_race, segment.segment_type]

    return jsonify(json_dict)


@app.route('/race-detail/comparison_visualisation', methods=['POST'])
def get_comparison_visualisation():
    race_name = request.form['race_name']
    comparison_race_name = request.form['comparison_race_name']
    segment_type = request.form['segment_type']

    output_folder = st.files["output_folder"]
    filename = f"{race_name}_{comparison_race_name}_{segment_type}.html"
    dir_filename = os.path.join(output_folder, filename)

    if dir_filename not in glob.glob(f'{output_folder}/*.html'):
        RACE_INFERER.draw(race_name, comparison_race_name, segment_type, dir_filename)

    json_dict = {'filename': f"/static/output/{filename}"}

    return jsonify(json_dict)


@app.route('/race-detail/comparison_table', methods=['POST'])
def get_comparison_table():
    race_name = request.form['race_name']
    comparison_race_name = request.form['comparison_race_name']
    segment_type = request.form['segment_type']

    deniv_segment, length_segment, density_segment = RACE_INFERER.get_best_segment(race_name)
    segments = deniv_segment + length_segment + density_segment

    segment = None

    for segment_tuple in segments:
        if segment_tuple[0] == comparison_race_name and segment_tuple[1].segment_type == segment_type:
            segment = segment_tuple[1]
            break

    json_dict = {"seg1": segment.get_statistics(from_race=1), "seg2": segment.get_statistics(from_race=2)}

    return jsonify(json_dict)


@app.route('/race-detail/comparison_graphs', methods=['POST'])
def get_comparison_graphs():
    race_name = request.form['race_name']
    comparison_race_name = request.form['comparison_race_name']
    segment_type = request.form['segment_type']

    deniv_segment, length_segment, density_segment = RACE_INFERER.get_best_segment(race_name)
    segments = deniv_segment + length_segment + density_segment

    segment = None

    for segment_tuple in segments:
        if segment_tuple[0] == comparison_race_name and segment_tuple[1].segment_type == segment_type:
            segment = segment_tuple[1]
            break

    start = segment.points1[0].distance / 1000
    stop = segment.points1[-1].distance / 1000

    json_dict = {'start': start, 'stop': stop}

    return jsonify(json_dict)


if __name__ == '__main__':
    app.run()
