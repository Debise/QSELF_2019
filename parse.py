from fitparse import FitFile
import os
import numpy as np
import pandas as pd
import gmplot 
import matplotlib.pyplot as plt
import glob

verbose = 0


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


def parse_all_to_pickle(draw_all):

    if draw_all:
        gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 13)

    for filename in glob.glob("*.fit"):

        pickle_file = "../pickle_activity/" + filename.replace('.fit', '.pkl')

        if glob.glob(pickle_file):
            #print(filename, ": already parsed")

            if draw_all:
                df_norm = pd.read_pickle(pickle_file)

        else:
            #print(filename, ": will be parsed")
            df = parse_fit_file(filename)
            df_norm = normalize_df(df)

            df_norm.to_pickle(pickle_file)

        if draw_all:
            gmap3.plot(df_norm["position_lat"], df_norm["position_long"], 'cornflowerblue', edge_width=2.5)
            # gmap3.scatter(dx, dy, '# FF0000', size=4, marker=False)  # too slow

    if draw_all:
        gmap3.draw("../output/all_run.html")



def compare_all_vs_one():

    os.chdir("../pickle_activity")
    df1 = pd.read_pickle("2019-04-09-08-29-05.pkl")#all vs this one

    # 2018-12-20-16-42-55.pkl
    # 2019-03-12-08-32-49.pkl
    # 2018-11-29-18-09-16.pkl
    # 2019-03-18-17-25-10.pkl

    filename = "2019-03-25-17-24-10.pkl"
    if 1:
    #for filename in glob.glob("*.pkl"):

        df2 = pd.read_pickle(filename)
        print(filename)

        gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)

        c1 = np.array(df1[["position_lat", "position_long"]]).T
        c2 = np.array(df2[["position_lat", "position_long"]]).T

        gmap3.plot(c1[0,:], c1[1,:], 'cornflowerblue', edge_width=2.5)
        gmap3.plot(c2[0,:], c2[1,:], 'green', edge_width=2.5)


        # Traitement...
        segment = extract_segment(c1, c2)

        #todo segment fusion or drop (if small split or too short)

        #Plot segment
        for array in segment:
            gmap3.plot(c1[0,array], c1[1,array], 'red', edge_width=4)

        gmap3.draw("../output/" + filename + ".html")


def extract_segment(c1, c2):

    SIZE = 10
    STEP = 5
    xi1 = np.zeros(c1.shape[1])
    xi2 = np.zeros(c2.shape[1])

    print(c2.shape[1])

    for i2 in range(0, c2.shape[1] - SIZE, STEP):
        # print(i2)

        for i1 in range(0, c1.shape[1] - SIZE, 1):

            dist2 = np.linalg.norm(c1[:, i1:i1 + SIZE] - c2[:, i2:i2 + SIZE])

            if dist2 <= 0.00089443:
                xi1[i1:i1 + SIZE] += 1
                xi2[i2:i2 + SIZE] += 1
    """segment extractor (list of segment)"""
    where = np.where(xi1 > 2)[0]
    print("where:", where.shape)
    # print(where)
    # plt.scatter(where,where)
    # plt.show()
    diff = np.diff(where) > 1
    # print("diff:",diff)
    if (diff == False).all():
        splitted = [where]

    else:
        sep = np.argwhere(diff).T[0]
        print("separator:", sep)
        splitted = np.split(where, sep + 1)
        # print("splitted:", splitted)

    return splitted


def main():

    os.chdir("activity")

    """parse all fit file to pickle file and plot all on one map"""
    parse_all_to_pickle(False)

    compare_all_vs_one()

if __name__ == "__main__":
    # execute only if run as a script
    main()
