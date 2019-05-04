from fitparse import FitFile
import os
import numpy as np
import pandas as pd
import gmplot 
import matplotlib.pyplot as plt
import pickle
import glob

def parse_fit_file(filename):
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

def dist(ax, ay, bx, by):

    return np.sum(np.power(ax-bx,2) + np.power(ay-by,2))

def main():

    os.chdir("activity")

    """parse all fit file to pickle file and plot all on one map"""
    parse_all_to_pickle()

    """Compare two runs"""
    if 0:
        gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
        df1 = parse_it("2019-02-18-18-02-48.fit")#("2018-11-29-18-09-16.fit")
        df2 = parse_it("2018-12-20-16-42-55.fit")

        df1 = normalize_df(df1)
        df2 = normalize_df(df2)

        gmap3.plot(df1["position_lat"], df1["position_long"], 'cornflowerblue', edge_width=2.5)
        gmap3.plot(df2["position_lat"], df2["position_long"], 'green', edge_width=2.5)

        x1 = np.array(df1["position_lat"])
        y1 = np.array(df1["position_long"])
        x2 = np.array(df2["position_lat"])
        y2 = np.array(df2["position_long"])

        # Traitement...

        SIZE = 20
        STEP = 5

        xi1 = np.zeros(x1.shape)
        yi1 = np.zeros(y1.shape)
        xi2 = np.zeros(x2.shape)
        yi2 = np.zeros(y2.shape)

        for i2 in range(0, x2.shape[0] - SIZE, STEP):
            #print(i2)
            for i1 in range(0, x1.shape[0] - SIZE, 1):

                disti = dist(x1[i1:i1+SIZE],y1[i1:i1+SIZE],x2[i2:i2+SIZE],y2[i2:i2+SIZE])
                #plt.scatter(i,disti)

                if disti<=0.0000015:#0.000001:
                    xi1[i1:i1 + SIZE] += 1
                    xi2[i2:i2 + SIZE] += 1

                    #x = (x1[i1:i1+SIZE]+x2[i2:i2+SIZE]) /2
                    #y = (y1[i1:i1+SIZE]+y2[i2:i2+SIZE]) / 2

        gmap3.plot(x1[xi1>0], y1[xi1>0], 'red', edge_width=4)

        #gmap3.plot(x, y, 'red', edge_width=4)
        #gmap3.plot(x2[j:j + SIZE], y2[j:j + SIZE], 'red', edge_width=4)


        gmap3.draw("../output/two_run.html")


def parse_all_to_pickle():
    gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
    for filename in glob.glob("*.fit"):

        pickle_file = "../pickle_activity/" + filename.replace('.fit', '.pkl')

        if glob.glob(pickle_file):
            print(filename, ": already parsed")

            df_norm = pd.read_pickle(pickle_file)

        else:
            print(filename, ": will be parsed")
            df = parse_fit_file(filename)
            df_norm = normalize_df(df)

            df_norm.to_pickle(pickle_file)

        gmap3.plot(df_norm["position_lat"], df_norm["position_long"], 'cornflowerblue', edge_width=2.5)
        # gmap3.scatter(dx, dy, '# FF0000', size=4, marker=False)  # too slow
    gmap3.draw("../output/all_run.html")


if __name__ == "__main__":
    # execute only if run as a script
    main()
