from src.segment_comparator import SegmentComparator
from src.race_comparator import RaceComparator
from src.race_manager import RaceManager
from src.segment import Segment
import settings as st
import pickle
from gmplot import GoogleMapPlotter
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


class RaceInferer:

    def __init__(self):

        self.race_manager = RaceManager.load()

        self.deniv_segment = {}  # each entry (for a given refRace) contains a tuple (matchingRaceName, MatchingSegment)
        self.length_segment = {}
        self.density_segment = {}

    def save(self):
        filename = os.path.join(st.files["pickle_class_folder"], "RaceInferer.pkl")
        pickle.dump(self, open(filename, "wb"))

    @staticmethod
    def load():
        filename = os.path.join(st.files["pickle_class_folder"], "RaceInferer.pkl")
        race_inferer = pickle.load(open(filename, "rb"))

        return race_inferer

    def find_race_deniv(self, referential_race_name):

        matching_race_segment = []

        deniv_seg = self.race_manager.best_denivelation_segment[referential_race_name]

        for race_name in self.race_manager.races:
            if race_name == referential_race_name:
                continue

            race = self.race_manager.races[race_name]

            matches = self.find_matching_race_segment(race, deniv_seg, "denivelation")

            if len(matches) > 0:

                if len(matches) > 1:
                    continue

                # TODO apply more restrictive selection/filtering ?
                if len(matches[0].points1) > 0.9 * len(deniv_seg.points1):
                    # only if the given match is more than 90% of the length of the reference seg
                    matching_race_segment.append((race_name, matches[0]))

        self.deniv_segment[referential_race_name] = matching_race_segment

    def find_race_length(self, referential_race_name):

        matching_race_segment = []

        length_seg = self.race_manager.best_length_segment[referential_race_name]

        for race_name in self.race_manager.races:
            if race_name == referential_race_name:
                continue

            race = self.race_manager.races[race_name]

            matches = self.find_matching_race_segment(race, length_seg, "length")

            if len(matches) > 0:

                if len(matches) > 1:
                    continue

                # TODO apply more restrictive selection/filtering ?
                if len(matches[0].points1) > 0.9 * len(length_seg.points1):
                    # only if the given match is more than 90% of the length of the reference seg
                    matching_race_segment.append((race_name, matches[0]))

        self.length_segment[referential_race_name] = matching_race_segment

    def find_race_density(self, referential_race_name):
        matching_race_segment = []
        density_seg = self.race_manager.best_density_segment[referential_race_name]

        for race_name in self.race_manager.races:
            if race_name == referential_race_name:
                continue

            race = self.race_manager.races[race_name]

            matches = self.find_matching_race_segment(race, density_seg, "density")

            if len(matches) > 0:

                if len(matches) > 1:
                    continue

                # TODO apply more restrictive selection/filtering ?
                if len(matches[0].points1) > 0.9 * len(density_seg.points1):
                    # only if the given match is more than 90% of the length of the reference seg
                    matching_race_segment.append((race_name, matches[0]))

        self.density_segment[referential_race_name] = matching_race_segment

    def draw_denivelation_segment(self, referential_race_name):
        deniv_segments = self.deniv_segment[referential_race_name]

        if deniv_segments is None:
            print("Sorry can't draw deniv_segment, not avalaible")
        else:

            race = self.race_manager.races[referential_race_name]
            gmap3 = self.draw_race_and_matches(race, deniv_segments)

            filename = os.path.join(st.files["output_folder"], f"best_deniv_matches_for_{referential_race_name}.html")
            gmap3.draw(filename)

    def draw_density_segment(self, referential_race_name):
        density_segments = self.density_segment[referential_race_name]

        if density_segments is None:
            print("Sorry can't draw density_segment, not avalaible")
        else:

            race = self.race_manager.races[referential_race_name]
            gmap3 = self.draw_race_and_matches(race, density_segments)

            filename = os.path.join(st.files["output_folder"], f"best_density_matches_for_{referential_race_name}.html")
            gmap3.draw(filename)

    def draw_length_segment(self, referential_race_name):
        length_segments = self.length_segment[referential_race_name]

        if length_segments is None:
            print("Sorry can't draw length_segment, not avalaible")
        else:

            race = self.race_manager.races[referential_race_name]
            gmap3 = self.draw_race_and_matches(race, length_segments)

            filename = os.path.join(st.files["output_folder"], f"best_length_matches_for_{referential_race_name}.html")
            gmap3.draw(filename)

    def draw_race_and_matches(self, race, matches):
        if GOOGLE_MAP_API_KEY is None:
            gmap3 = GoogleMapPlotter(46.98, 6.89, 14)
        else:
            gmap3 = GoogleMapPlotter(46.98, 6.89, 14, apikey=GOOGLE_MAP_API_KEY)

        gmap3.plot(race.df.position_lat, race.df.position_long, 'cornflowerblue', edge_width=2.5)

        for (race_name, match) in matches:
            match.draw('yellow', gmap3=gmap3)

        return gmap3

    def find_matching_race_segment(self, race, best_segment, segment_type):

        # Make a big segment out of a race (heavy but less code needed...)
        race_comparator = RaceComparator(race, race)
        race_comparator.extract_segment()
        segments = race_comparator.segments


        race_as_segment = segments[0]

        segment_comparator = SegmentComparator(best_segment, race_as_segment)
        segment_comparator.extract_segment(segment_type)
        matches = segment_comparator.segments

        return matches

    def get_statistics_from_deniv_seg(self, referential_race_name):
        from_race = []

        # from the given ref race
        deniv_segment_ref_race = self.race_manager.best_denivelation_segment[referential_race_name]
        from_race.append((referential_race_name, deniv_segment_ref_race.get_statistics(from_race=1)))

        # from the segment matching races
        for (name, seg) in self.deniv_segment[referential_race_name]:
            from_race.append((name, seg.get_statistics(from_race=1)))

        return from_race

    def get_statistics_from_density_seg(self, referential_race_name):
        from_race = []

        # from the given ref race
        density_segment_ref_race = self.race_manager.best_density_segment[referential_race_name]
        from_race.append((referential_race_name, density_segment_ref_race.get_statistics(from_race=1)))

        # from the segment matching races
        for (name, seg) in self.density_segment[referential_race_name]:
            from_race.append((name, seg.get_statistics(from_race=1)))

        return from_race

    def get_statistics_from_length_seg(self, referential_race_name):
        from_race = []

        # from the given ref race
        length_segment_ref_race = self.race_manager.best_length_segment[referential_race_name]
        from_race.append((referential_race_name, length_segment_ref_race.get_statistics(from_race=1)))

        # from the segment matching races
        for (name, seg) in self.length_segment[referential_race_name]:
            from_race.append((name, seg.get_statistics(from_race=1)))

        return from_race
