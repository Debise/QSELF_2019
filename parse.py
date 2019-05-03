from fitparse import FitFile
import os
import numpy as np
import pandas as pd
import gmplot 


def parse_it(filename):
    fitfile = FitFile(filename)
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

    return df


def normalize_df(df):
    df.position_lat = df.position_lat.apply(lambda x: semi_to_degree(x))
    df.position_long = df.position_long.apply(lambda x: semi_to_degree(x))
    df.altitude = df.altitude.apply(lambda x: x / 10)
    df.speed = df.speed.apply(lambda x: x / 1000)

    return df


def semi_to_degree(s):
    return s * (180.0 / 2**31)


fitfile_1 = os.path.join('activity/2019-04-09-08-29-05.fit')
fitfile_2 = os.path.join('activity/2019-04-28-16-54-19.fit')

fit1_df = normalize_df(parse_it(fitfile_1))
fit2_df = normalize_df(parse_it(fitfile_2))

dx1, dy1 = fit1_df.position_lat.values, fit1_df.position_long.values
dx2, dy2 = fit2_df.position_lat.values, fit2_df.position_long.values

gmap3 = gmplot.GoogleMapPlotter(np.mean(dx1), np.mean(dy1), 14)

# scatter method of map object  
# scatter points on the google map 
gmap3.scatter(dx1, dy1, '# FF0000', size=4, marker=False)
  
# Plot method Draw a line in between given coordinates
gmap3.plot(dx2, dy2, 'cornflowerblue', edge_width=2.5)
  
gmap3.draw("output/map.html")


print("Nb point:", len(dx1))
print("Nb point:", len(dx2))
