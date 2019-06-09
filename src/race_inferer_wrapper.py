
from src.race_inferer import RaceInferer

class RaceInfererWrapper:

    def __init__(self):

        self.RACE_INFERER = RaceInferer.load()

    def get_best_segment(self, referential_race_name):

        """return 3 lists of tuples : (matchingRaceName, MatchingSegment)"""

        return self.RACE_INFERER.deniv_segment[referential_race_name], self.RACE_INFERER.length_segment[referential_race_name], self.RACE_INFERER.density_segment[referential_race_name]