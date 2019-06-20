from src.segment import Segment
import os
import numpy as np
import settings as st
from gmplot import GoogleMapPlotter

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


class RaceComparator:

    def __init__(self, race1, race2):
        self.race1 = race1
        self.race2 = race2
        self.segments = []
        self.name = '{}_vs_{}'.format(self.race1.name, self.race2.name)

    def __str__(self):
        string = "Comparison {}\n\n".format(self.name)
        string += "List of segments : \n\n"

        for i, segment in enumerate(self.segments):
            string += "Segment N° {} ({} points) \n".format(i, len(segment.points1))
            string += str(segment)

        return string

    def extract_segment(self):
        size = 10
        step = 5
        epsilon = 0.00089443

        df1 = self.race1.df
        df2 = self.race2.df

        c1 = df1[["timestamp", "position_lat", "position_long", "altitude", "distance"]].values.T
        c2 = df2[["timestamp", "position_lat", "position_long", "altitude", "distance"]].values.T

        c1_matched_c2 = np.zeros(c1.shape[1])
        mean_trace = np.zeros((4, c1.shape[1]))  # [pos_lat, pos_long, altitude, distance]
        timestamps_trace = np.zeros((2, c1.shape[1]), dtype='object')

        for i2 in range(0, c2.shape[1] - size, step):
            for i1 in range(0, c1.shape[1] - size, 1):

                dist2 = np.linalg.norm(c1[1:3, i1:i1 + size] - c2[1:3, i2:i2 + size])

                if dist2 <= epsilon:
                    c1_matched_c2[i1:i1 + size] += 1

                    mean_trace[:3, i1:i1 + size] = (c1[1:4, i1:i1 + size] + c2[1:4, i2:i2 + size]) / 2
                    mean_trace[3, i1:i1 + size] = c1[4,
                                                  i1:i1 + size]  # pour la distance on ne calcule pas la moyenne --> ça fausse tout

                    timestamps_trace[:, i1:i1 + size] = [c1[0, i1:i1 + size], c2[0, i2:i2 + size]]

        # Segment extractor (list of segment)
        where = np.where(c1_matched_c2 > 1)[0]
        diff = np.diff(where) > 1

        if diff is False:
            splitted = [where]
        else:
            sep = np.argwhere(diff).T[0]
            splitted = np.split(where, sep + 1)

        ret = [mean_trace[:, i] for i in splitted]
        times = [timestamps_trace[:, i] for i in splitted]

        # Drop segments shorter than 20
        segments_filtered = [i for i in ret if i.shape[1] > 40]
        times_filtered = [i for i in times if i.shape[1] > 40]

        # drop les segments qui ne sont pas très correct (match mais pas de façon continue)
        retour = []
        times_2 = []

        for segment, time in zip(segments_filtered, times_filtered):
            diff = np.diff(segment[3, :])
            if np.max(diff) < 50:
                # valide si moins de 50m entre 2 points
                retour.append(segment)
                times_2.append(time)

        # Pack for storage
        for seg in zip(segments_filtered, times_filtered):
            positions = seg[0]
            timestamps1 = seg[1][0]
            timestamps2 = seg[1][1]
            self.segments.append(Segment(positions, timestamps1, timestamps2, self.race1.points, self.race2.points, "primitive"))

    def draw(self):
        if GOOGLE_MAP_API_KEY is None:
            gmap3 = GoogleMapPlotter(46.98, 6.89, 14)
        else:
            gmap3 = GoogleMapPlotter(46.98, 6.89, 14, apikey=GOOGLE_MAP_API_KEY)

        self.race1.draw(color='cornflowerblue', gmap3=gmap3)
        self.race2.draw(color='limegreen', gmap3=gmap3)

        # Plot segment
        for segment in self.segments:
            segment.draw(color='red', gmap3=gmap3)

        output_folder = st.files["output_folder"]
        filename = f'{output_folder}/{self.name}.html'

        gmap3.draw(filename)
