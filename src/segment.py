import numpy as np


class Segment:

    def __init__(self, positions, times1, times2, points1, points2, segment_type):
        self.positions = positions
        self.times1 = times1
        self.times2 = times2
        self.points1 = points1
        self.points2 = points2
        self.keep_segment_points()
        self.segment_type = segment_type

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

    def get_statistics(self, from_race=1, verbose=False):

        if from_race == 1:
            points = self.points1
        else:
            points = self.points2

        race_time = points[-1].timestamp - points[0].timestamp
        minutes = race_time.seconds / 60
        hours = minutes / 60
        hours_str = f'{int(hours)} hour(s) and {(minutes - (int(hours) * 60)):.2f} minutes'

        speed_array = np.array([i.speed for i in points if i.speed > 0])
        average_speed = np.mean(speed_array)
        max_speed = np.max(speed_array)
        min_speed = np.min(speed_array)
        std_speed = np.std(speed_array)

        altitude_array = np.array([i.altitude for i in points])
        heights_difference = np.max(altitude_array) - np.min(altitude_array)

        derivative = np.diff(altitude_array)
        derivative[derivative < 0] = 0
        positive_denivelation = np.sum(derivative)  # only positive !

        distance = points[-1].distance - points[0].distance
        km_distance = distance / 1000

        heart_rate_array = np.array([i.heart_rate for i in points])
        average_heart_rate = np.mean(heart_rate_array)

        stats = {
            'Race time': hours_str,
            'Average speed': f'{average_speed:.2f} m/s ({(average_speed * 3.6):.2f} km/h)',
            'Max speed': f'{max_speed:.2f} m/s ({(max_speed * 3.6):.2f} km/h)',
            'Min speed': f'{min_speed:.2f} m/s ({(min_speed * 3.6):.2f} km/h)',
            'Speed standard deviation': f'{std_speed:.2f}',
            'Heights difference': f'{heights_difference:.2f} m',
            'Positive denivelation': f'{positive_denivelation:.2f} m',
            'Total distance': f'{distance:.2f} m ({km_distance:.2f} km)',
            'Average HR': f'{average_heart_rate:.2f} bpm'
        }

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

        return stats
