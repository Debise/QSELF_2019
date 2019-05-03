from fitparse import FitFile
import os
import numpy as np
import pandas as pd
import gmplot 
import matplotlib.pyplot as plt

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

def dist(ax, ay, bx, by):

    return np.sum(np.power(ax-bx,2) + np.power(ay-by,2))

def main():

    os.chdir("activity")


    """ALL run on one plot"""
    if 0:
        gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
        for filename in os.listdir(os.getcwd()):

            df = parse_it(filename)
            df_norm = normalize_df(df)
            print(filename)

            gmap3.plot(df_norm["position_lat"], df_norm["position_long"],'cornflowerblue', edge_width=2.5)
            #gmap3.scatter(dx, dy, '# FF0000',size = 4, marker = False )

        gmap3.draw("../output/all_run.html")

    gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
    df1 = parse_it("2018-11-29-18-09-16.fit")
    df1 = normalize_df(df1)
    df2 = parse_it("2018-12-20-16-42-55.fit")
    df2 = normalize_df(df2)

    gmap3.plot(df1["position_lat"], df1["position_long"], 'cornflowerblue', edge_width=2.5)
    gmap3.plot(df2["position_lat"], df2["position_long"], 'green', edge_width=2.5)

    x1 = np.array(df1["position_lat"])
    y1 = np.array(df1["position_long"])
    x2 = np.array(df2["position_lat"])
    y2 = np.array(df2["position_long"])

    # Traitement...
    for i in range(x1.shape[0] - 10):

        disti = dist(x1[i:i+10],y1[i:i+10],x2[100:110],y2[100:110])
        plt.scatter(i,disti)

        if disti<=0.000001:
            gmap3.scatter(x1[i:i+10], y1[i:i+10], 'purple', size=4, marker=False)

    plt.show()


    gmap3.plot(x2[100:110],y2[100:110], 'red', edge_width=2.5)


    gmap3.draw("../output/two_run.html")

if __name__ == "__main__":
    # execute only if run as a script
    main()
