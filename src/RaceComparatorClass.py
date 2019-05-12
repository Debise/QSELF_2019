import numpy as np
import gmplot


class RaceComparator:

    def __init__(self, race1, race2):
        self.race1 = race1
        self.race2 = race2
        self.segments = []
        self.name = '{}_vs_{}'.format(self.race1.name, self.race2.name)

    def extract_segment(self):
        size = 10
        step = 5
        epsilon = 0.00089443

        df1 = self.race1.df
        df2 = self.race2.df

        c1 = df1[["position_lat", "position_long"]].values.T
        c2 = df2[["position_lat", "position_long"]].values.T

        c1_matched_c2 = np.zeros(c1.shape[1])
        mean_trace = np.zeros(c1.shape)

        for i2 in range(0, c2.shape[1] - size, step):
            for i1 in range(0, c1.shape[1] - size, 1):
                dist2 = np.linalg.norm(c1[:, i1:i1 + size] - c2[:, i2:i2 + size])

                if dist2 <= epsilon:
                    c1_matched_c2[i1:i1 + size] += 1
                    mean_trace[:, i1:i1 + size] = (c1[:, i1:i1 + size] + c2[:, i2:i2 + size]) / 2

        # Segment extractor (list of segment)
        where = np.where(c1_matched_c2 > 1)[0]
        diff = np.diff(where) > 1

        if diff is False:
            splitted = [where]
        else:
            sep = np.argwhere(diff).T[0]
            splitted = np.split(where, sep + 1)

        ret = [mean_trace[:, i] for i in splitted]

        self.segments = ret

    def draw(self):
        gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)

        self.race1.draw(color='cornflowerblue', gmap3=gmap3)
        self.race2.draw(color='green', gmap3=gmap3)

        # Plot segment
        for segment in self.segments:
            gmap3.plot(segment[0, :], segment[1, :], 'red', edge_width=4)

        filename = 'output/{}.html'.format(self.name)

        gmap3.draw(filename)
