from src.race import Race
from src.race_comparator import RaceComparator
import glob
import pickle
import os
import settings as st


class RaceManager:

    def __init__(self):
        self.races = {}
        self.race_comparators = {}

    def read_all_races(self):
        activity_folder = st.files["activity_folder"]

        for filename in glob.glob(f'{activity_folder}/*.fit'):
            race = Race(filename)
            race.parse_fit_file()
            race.df_to_point_list()
            self.races[race.name] = race

    def save(self):
        filename = os.path.join(st.files["pickle_class_folder"], "RaceManager.pkl")
        pickle.dump(self, open(filename, "wb"))

    @staticmethod
    def load():
        filename = os.path.join(st.files["pickle_class_folder"], "RaceManager.pkl")
        race_manager = pickle.load(open(filename, "rb"))

        return race_manager

    def compare_all_vs_one(self, referential_race_name, verbose=0):
        races = self.races
        referential_race = races.pop(referential_race_name)
        races = races.values()

        for race in races:

            if verbose:
                print(race.filename)

            # Treatment...
            race_comparator = RaceComparator(referential_race, race)
            race_comparator.extract_segment()
            segments = race_comparator.segments

            if verbose:
                print("Number of segment found      :", len(segments))
                print(race_comparator)

            race_comparator.draw()
            self.race_comparators[race_comparator.name] = race_comparator
