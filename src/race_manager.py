from src.race import Race
from src.race_comparator import RaceComparator
from src.best_segment import BestSegment
import glob
import pickle
import os
import numpy as np
from gmplot import GoogleMapPlotter
import settings as st

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


class RaceManager:

    def __init__(self):
        self.races = {}  # str name
        self.race_comparators = {}
        self.all_seg_of_one_race = {}

        # density related
        self.race_segment_density = {}
        self.race_mean_seg_density = {}
        self.race_density_delta = {}

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
        races = dict(self.races)  # copy
        referential_race = races.pop(referential_race_name)
        races = races.values()

        all_segment = []
        for race in races:

            if verbose:
                print(race.filename)

            # Treatment...
            race_comparator = RaceComparator(referential_race, race)
            race_comparator.extract_segment()
            segments = race_comparator.segments
            all_segment.extend(segments)

            if verbose:
                print("Number of segment found      :", len(segments))
                print(race_comparator)

            race_comparator.draw()
            self.race_comparators[race_comparator.name] = race_comparator

        print("Total number of segment found      :", len(all_segment))

        self.all_seg_of_one_race[referential_race_name] = all_segment

    def segment_density(self, referential_race_name, verbose=0):
        all_segments = list(self.all_seg_of_one_race[referential_race_name])

        points = np.array(all_segments[0].positions[:2, :])

        for segment in all_segments[1:]:
            try:
                points = np.append(points, segment.positions[:2, :], axis=1)
            except:
                print("Probably zero size array...")

        max_lat = np.max(points[0, :])
        max_long = np.max(points[1, :])
        min_lat = np.min(points[0, :])
        min_long = np.min(points[1, :])

        # print(max_lat,max_long,min_lat,min_long)

        delta = 0.0005  # degré

        lat = np.arange(min_lat, max_lat, delta)
        long = np.arange(min_long, max_long, delta)
        density = np.zeros([3, lat.shape[0] * long.shape[0]])  # [lat,long,nbpoint]

        i = 0
        for x in lat:
            for y in long:
                # parcours et remplissage de la "grid" de densité

                density[0, i] = x
                density[1, i] = y

                for segment in all_segments:

                    seg = segment.positions

                    x_less = np.where(seg[0, :] >= (x - delta / 2))
                    x_more = np.where(seg[0, :] < (x + delta / 2))
                    count_x = np.intersect1d(x_less, x_more)

                    y_less = np.where(seg[1, :] >= (y - delta / 2))
                    y_more = np.where(seg[1, :] < (y + delta / 2))
                    count_y = np.intersect1d(y_less, y_more)

                    valid_coordinate = np.intersect1d(count_x, count_y).shape[0]

                    if valid_coordinate > 0:
                        # on ajoute 1 si le segment est dedans (la case de la grid)
                        density[2, i] = density[2, i] + 1

                i += 1

        # repasser tous les segment et ajouter leur propre densité max,min,mean pour chacun
        max_seg_density = dict()
        min_seg_density = dict()
        mean_seg_density = dict()
        seg_present_in = dict()

        for segment in all_segments:
            seg_name = segment.times1[
                0]  # FIXME convention --> le nom du segment c'est le timestamp de début de la course 1 (devrait ^etre unique)
            min_seg_density[seg_name] = 100
            max_seg_density[seg_name] = 0
            mean_seg_density[seg_name] = 0
            seg_present_in[seg_name] = 0

        i = 0
        for x in lat:
            for y in long:
                # parcours de la "grid" et regarder combien de point il y a pour chaque segment

                for segment in all_segments:

                    seg_name = segment.times1[0]
                    seg = segment.positions

                    x_less = np.where(seg[0, :] >= (x - delta / 2))
                    x_more = np.where(seg[0, :] < (x + delta / 2))
                    count_x = np.intersect1d(x_less, x_more)

                    y_less = np.where(seg[1, :] >= (y - delta / 2))
                    y_more = np.where(seg[1, :] < (y + delta / 2))
                    count_y = np.intersect1d(y_less, y_more)

                    valid_coordinate = np.intersect1d(count_x, count_y).shape[0]

                    if valid_coordinate > 0:
                        if density[2, i] > max_seg_density[seg_name]:
                            # si le segment est dedans (la case de la grid)
                            max_seg_density[seg_name] = density[2, i]

                        if density[2, i] < min_seg_density[seg_name]:
                            min_seg_density[seg_name] = density[2, i]

                        mean_seg_density[seg_name] += density[2, i]
                        seg_present_in[seg_name] += 1

                i += 1

        for segment in all_segments:
            seg_name = segment.times1[0]

            mean_seg_density[seg_name] = mean_seg_density[seg_name] / seg_present_in[seg_name]

        # print(max_seg_density)
        # print(min_seg_density)
        # print(seg_present_in)
        # print(mean_seg_density)

        # Print denstiy seg map
        gmap3 = GoogleMapPlotter(46.98, 6.89, 14, apikey=GOOGLE_MAP_API_KEY)

        self.races[referential_race_name].draw(color='cornflowerblue', gmap3=gmap3)

        # Plot segment
        for segment in all_segments:
            segment.draw(color='purple', gmap3=gmap3)

        # Plot density grid
        for i in range(density.shape[1]):
            if density[2, i] > 2:
                gmap3.scatter([density[0, i]], [density[1, i]], "yellow", size=density[2, i], marker=False)

        filename = os.path.join(st.files["output_folder"], f"seg_density_{referential_race_name}.html")
        gmap3.draw(filename)
        ###

        self.race_segment_density[referential_race_name] = density
        self.race_density_delta[referential_race_name] = delta
        self.race_mean_seg_density[referential_race_name] = mean_seg_density

    def race_vs_segments(self, referential_race_name, verbose=0):

        df = self.races[referential_race_name].df
        referential_race = df[["timestamp", "position_lat", "position_long", "altitude", "distance"]].values.T
        all_segments = list(self.all_seg_of_one_race[referential_race_name])

        # sort by length
        all_segments.sort(key=lambda x: len(x.points1), reverse=True)
        # [print(len(seg.points1)) for seg in all_segments]

        segment_density = self.race_segment_density[referential_race_name]
        mean_seg_density = self.race_mean_seg_density[referential_race_name]
        density_delta = self.race_density_delta[referential_race_name]

        # Extract the more interesting segment for the given race

        bestSegment = BestSegment(referential_race_name, all_segments, mean_seg_density)
        best_density_segment = bestSegment.get_density_segment()
        best_denivelation_segment = bestSegment.get_denivelation_segment()
        best_length_segment = bestSegment.get_length_segment()

        # print(len(best_denivelation_segment.points1))
        # print(len(best_length_segment.points1))
        # print(len(best_density_segment.points1))

        # TODO save these seg as argument...

        bestSegment.draw()
