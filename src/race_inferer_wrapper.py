from src.race_inferer import RaceInferer
import os
from gmplot import GoogleMapPlotter

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


class RaceInfererWrapper:

    def __init__(self):
        self.race_inferer = RaceInferer.load()

    def get_best_segment(self, referential_race_name):
        """return 3 lists of tuples : (matchingRaceName, MatchingSegment)"""

        return self.race_inferer.deniv_segment[referential_race_name], self.race_inferer.length_segment[
            referential_race_name], self.race_inferer.density_segment[referential_race_name]

    def draw(self, referential_race_name, comparison_race_name, segment_type, filename):
        """Draw both races and the corresponding best segment"""
        race_manager = self.race_inferer.race_manager
        referential_race = race_manager.races[referential_race_name]
        comparison_race = race_manager.races[comparison_race_name]

        deniv_segment, length_segment, density_segment = self.get_best_segment(referential_race_name)
        segments = deniv_segment + length_segment + density_segment

        segment = None

        for segment_tuple in segments:
            if segment_tuple[0] == comparison_race_name and segment_tuple[1].segment_type == segment_type:
                segment = segment_tuple[1]
                break

        if GOOGLE_MAP_API_KEY is None:
            gmap3 = GoogleMapPlotter(46.98, 6.89, 14)
        else:
            gmap3 = GoogleMapPlotter(46.98, 6.89, 14, apikey=GOOGLE_MAP_API_KEY)

        gmap3.plot(referential_race.df.position_lat, referential_race.df.position_long, 'cornflowerblue',
                   edge_width=2.5)
        gmap3.plot(comparison_race.df.position_lat, comparison_race.df.position_long, 'limegreen',
                   edge_width=2.5)

        segment.draw('red', gmap3)

        gmap3.draw(filename)
