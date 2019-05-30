from src.SegmentClass import Segment
import numpy as np


class SegmentComparator:

    def __init__(self, segment1, segment2):
        self.segment1 = segment1
        self.segment2 = segment2
        self.segments = []
        self.name = '{}_&_{}'.format(self.segment1.times1[0], self.segment2.times1[0])

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

        c1 = self.segment1.positions#"position_lat", "position_long", "altitude", "distance"
        c2 = self.segment2.positions

        c1_matched_c2 = np.zeros(c1.shape[1])
        mean_trace = np.zeros((4, c1.shape[1])) # [pos_lat, pos_long, altitude, distance]
        timestamps_trace = np.zeros((2, c1.shape[1]), dtype='object')

        for i2 in range(0, c2.shape[1] - size, step):
            for i1 in range(0, c1.shape[1] - size, 1):

                dist2 = np.linalg.norm(c1[0:2, i1:i1 + size] - c2[0:2, i2:i2 + size])

                if dist2 <= epsilon:
                    c1_matched_c2[i1:i1 + size] += 1

                    mean_trace[:3, i1:i1 + size] = (c1[0:3, i1:i1 + size] + c2[0:3, i2:i2 + size]) / 2
                    mean_trace[3, i1:i1 + size] = c1[3, i1:i1 + size] # pour la distance on ne calcule pas la moyenne --> ça fausse tout

                    timestamps_trace[:, i1:i1 + size] = [self.segment1.times1[i1:i1 + size], self.segment2.times1[i2:i2 + size]]

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

         #drop les segments qui ne sont pas très correct (match mais pas de façon continue)
        retour = []
        times_2 = []
        #print(len(ret),len(times))
        for segment, time in zip(segments_filtered, times_filtered):
            #print(segment.shape)
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
            self.segments.append(Segment(positions, timestamps1, timestamps2, self.segment1.points1, self.segment2.points1))
