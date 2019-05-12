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

    def save(self, re_parse=False):
        os.chdir("pickle_class")

        filename = "RaceManager.pkl"

        if re_parse:
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
                print("Segment length               :", [i.shape[1] for i in segments])

            # Drop segments shorter than 20
            segments_filtered = [i for i in segments if i.shape[1] > 20]

            if verbose:
                print("Number of filtered segment   :", len(segments_filtered))
                print("Filtered segment length      :", [i.shape[1] for i in segments_filtered])

            race_comparator.segments = segments_filtered
            race_comparator.draw()
            self.race_comparators[race_comparator.name] = race_comparator
