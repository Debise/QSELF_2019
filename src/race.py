from src.point import Point
from fitparse import FitFile
import os
import numpy as np
import pandas as pd
from gmplot import GoogleMapPlotter
import settings as st

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


class Race:

    def __init__(self, filename):
        self.filename = filename
        self.name = self.filename.split("/")[-1][:-4]
        self.df = None
        self.points = []

    def parse_fit_file(self):
        fitfile = FitFile(self.filename)
        fitfile.parse()

        records = fitfile.get_messages(name='record')
        records_dict = {}

        for record in records:
            for field in record.fields:
                if field.name not in records_dict.keys():
                    records_dict[field.name] = []

                records_dict[field.name].append(field.value)

        records_dict.pop('unknown_87', None)
        records_dict.pop('unknown_88', None)
        records_dict.pop('unknown_90', None)

        df = pd.DataFrame.from_dict(records_dict)

        self.df = self.normalize_df(df)

    def df_to_point_list(self):
        for r in self.df.values:
            point = Point(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11])
            self.points.append(point)

    def draw(self, color='cornflowerblue', gmap3=None):
        if gmap3 is None:
            if GOOGLE_MAP_API_KEY is None:
                gmap3 = GoogleMapPlotter(46.98, 6.89, 14)
            else:
                gmap3 = GoogleMapPlotter(46.98, 6.89, 14, apikey=GOOGLE_MAP_API_KEY)

        gmap3.plot(self.df.position_lat, self.df.position_long, color, edge_width=2.5)

        filename = os.path.join(st.files["output_folder"], f"{self.name}.html")
        gmap3.draw(filename)

    def get_statistics(self, verbose=False):
        race_time = self.points[-1].timestamp - self.points[0].timestamp
        minutes = race_time.seconds / 60
        hours = minutes / 60

        hours_str = f'{int(hours)} hour(s) and {(minutes - (int(hours) * 60)):.2f} minutes'

        average_speed = self.df.speed.mean()
        max_speed = self.df.speed.max()
        min_speed = self.df.speed[self.df.speed != 0].min()
        std_speed = self.df.speed.std()
        distances = [d / 1000 for d in self.df.distance.values.tolist()]
        speeds = [s * 3.6 for s in self.df.speed.values.tolist()]
        bpms = self.df.heart_rate.values.tolist()
        heights = self.df.altitude.values.tolist()

        heights_difference = self.df.altitude.max() - self.df.altitude.min()

        derivative = np.diff(np.array(self.df.altitude))
        derivative[derivative < 0] = 0
        positive_denivelation = np.sum(derivative)  # only positive !

        distance = self.points[-1].distance
        km_distance = distance / 1000

        average_heart_rate = self.df.heart_rate.mean()

        if verbose:
            print(f"{minutes} minutes")
            print(f"average speed : {average_speed} m/s")
            print(f"max speed : {max_speed} m/s")
            print(f"min speed : {min_speed} m/s")
            print(f"std speed : {std_speed}")
            print(f"heights_difference : {heights_difference} m")
            print(f"positive denivelation : {positive_denivelation} m")
            print(f"distance : {distance} m")
            print(f"average HR : {average_heart_rate} bpm")

        stats = {
            'Race time': hours_str,
            'Average speed': f'{average_speed:.2f} m/s ({(average_speed * 3.6):.2f} km/h)',
            'Max speed': f'{max_speed:.2f} m/s ({(max_speed * 3.6):.2f} km/h)',
            'Min speed': f'{min_speed:.2f} m/s ({(min_speed * 3.6):.2f} km/h)',
            'Speed standard deviation': f'{std_speed:.2f}',
            'Heights difference': f'{heights_difference:.2f} m',
            'Positive denivelation': f'{positive_denivelation:.2f} m',
            'Total distance': f'{distance} m ({km_distance:.2f} km)',
            'Average HR': f'{average_heart_rate:.2f} bpm',
            'distances': distances,
            'speeds': speeds,
            'bpms': bpms,
            'heights': heights
        }

        return stats

    @staticmethod
    def normalize_df(df):

        def semi_to_degree(s):
            return s * (180.0 / 2 ** 31)

        df.position_lat = df.position_lat.apply(lambda x: semi_to_degree(x))
        df.position_long = df.position_long.apply(lambda x: semi_to_degree(x))
        df.altitude = df.altitude.apply(lambda x: x / 10)
        df.speed = df.speed.apply(lambda x: x / 1000)

        return df
