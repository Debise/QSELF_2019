from src.RaceClass import Race
from src.RaceComparatorClass import RaceComparator
import glob
import pickle
import os


class RaceManager:

    def __init__(self):
        self.races = {}
        self.race_comparators = {}

    def read_all_races(self):
        os.chdir("activity")

        for filename in glob.glob('*.fit'):
            race = Race(filename)
            race.parse_fit_file()
            race.df_to_point_list()
            self.races[race.name] = race

        os.chdir("..")

    def save(self):
        os.chdir("pickle_class")

        filename = "RaceManager.pkl"

        pickle.dump(self, open(filename, "wb"))

        os.chdir("..")

    @staticmethod
    def load():
        os.chdir("pickle_class")

        filename = "RaceManager.pkl"

        race_manager = pickle.load(open(filename, "rb"))

        os.chdir("..")

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

            race_comparator.draw()
            self.race_comparators[race_comparator.name] = race_comparator
            print(race_comparator)

            break
