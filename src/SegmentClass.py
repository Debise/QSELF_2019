class Segment:

    def __init__(self, positions, times1, times2, points1, points2):
        self.positions = positions
        self.times1 = times1
        self.times2 = times2
        self.points1 = points1
        self.points2 = points2
        self.keep_segment_points()

    def __str__(self):
        string = ""

        for i, pos in enumerate(zip(self.positions[0], self.positions[1])):
            string += "\tPoint segment : {} : x = {}, y  = {}\n".format(self.times1[i], pos[0], pos[1])
            string += "\tPoint race 1 : {}\n".format(self.points1[i])
            string += "\tPoint race 2 : {}".format(self.points2[i])
            string += "\n\n"

            if i >= 8:
                string += "\t... (segment too long, show only 10 points)\n\n"
                string += "\tPoint segment : {} : x = {}, y  = {}\n".format(self.times1[-1], pos[0], pos[1])
                string += "\tPoint race 1 : {}\n".format(self.points1[-1])
                string += "\tPoint race 2 : {}".format(self.points2[-1])
                break

        return string

    def keep_segment_points(self):
        kept_points = []

        for time in self.times1:
            for point in self.points1:
                if time == point.timestamp:
                    kept_points.append(point)

        self.points1 = kept_points
        kept_points = []

        for time in self.times2:
            for point in self.points2:
                if time == point.timestamp:
                    kept_points.append(point)

        self.points2 = kept_points

    def draw(self, color, gmap3):
        gmap3.plot(self.positions[0, :], self.positions[1, :], color, edge_width=4)

