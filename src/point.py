class Point:

    def __init__(self, timestamp, position_lat, position_long, distance, enhanced_altitude,
                 altitude, enhanced_speed, speed, heart_rate, cadence, temperature, fractional_cadence):

        self.timestamp = timestamp
        self.position_lat = position_lat
        self.position_long = position_long
        self.distance = distance
        self.enhanced_altitude = enhanced_altitude
        self.altitude = altitude
        self.enhanced_speed = enhanced_speed
        self.speed = speed
        self.heart_rate = heart_rate
        self.cadence = cadence
        self.temperature = temperature
        self.fractional_cadence = fractional_cadence

    def __str__(self):
        return '{} : x = {}, y = {}'.format(self.timestamp, self.position_lat, self.position_long)
