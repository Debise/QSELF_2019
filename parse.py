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


def parse_all_to_pickle(draw_all=False):

    if draw_all:
        gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 13)

    for filename in glob.glob("*.fit"):

        pickle_file = "../pickle_activity/" + filename.replace('.fit', '.pkl')

        if glob.glob(pickle_file):
            # print(filename, ": already parsed")

            if draw_all:
                df_norm = pd.read_pickle(pickle_file)

        else:
            # print(filename, ": will be parsed")
            df = parse_fit_file(filename)
            df_norm = normalize_df(df)

            df_norm.to_pickle(pickle_file)

        if draw_all:
            gmap3.plot(df_norm["position_lat"], df_norm["position_long"], 'cornflowerblue', edge_width=2.5)
            # gmap3.scatter(dx, dy, '# FF0000', size=4, marker=False)  # too slow

    if draw_all:
        gmap3.draw("../output/all_run.html")


def density_map():
    os.chdir("../pickle_activity")

    gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 13.6)

    df1 = pd.read_pickle("2019-04-09-08-29-05.pkl")  # all vs this one
    all_runs = np.array(df1[["position_lat", "position_long"]]).T

    for filename in glob.glob("*.pkl"):

        if filename == "2019-04-09-08-29-05.pkl":
            continue


        df1 = pd.read_pickle(filename)

        #print(filename)

        c1 = np.array(df1[["position_lat", "position_long"]]).T

        #print(c1.shape)

        all_runs = np.append(all_runs, c1, axis=1)

    print(all_runs.shape)

    gmap3.plot(all_runs[0, :], all_runs[1, :], 'cornflowerblue', edge_width=2.5)

    max_lat = np.max(all_runs[0, :])
    max_long = np.max(all_runs[1, :])
    min_lat = np.min(all_runs[0, :])
    min_long = np.min(all_runs[1, :])

    print(min_lat, min_long, max_lat, max_long)

    inter = 50

    delta_lat = (max_lat - min_lat) / inter
    delta_long = (max_long - min_long) / inter

    lat = np.linspace(min_lat, max_lat, inter)
    long = np.linspace(min_long, max_long, inter)

    all_latitude = all_runs[0, :]
    all_longitude = all_runs[1, :]

    print(all_longitude.shape)
    print(all_latitude.shape)

    i=0
    for x in lat:
        i += 1

        less = np.where(all_latitude >= (x-delta_lat/2))
        more = np.where(all_latitude < (x + delta_lat / 2))
        count_x = np.intersect1d(less,more)

        for y in long:

            less = np.where(all_longitude >= (y - delta_long / 2))
            more = np.where(all_longitude < (y + delta_long / 2))
            count_y = np.intersect1d(less, more)

            valid_coordinate = np.intersect1d(count_x, count_y).shape[0]

            #print(i, len(count_x), len(count_y), valid_coordinate)

            if valid_coordinate != 0:
                gmap3.scatter([x], [y], "red", size=np.sqrt([valid_coordinate])[0]*8, marker=False)

    gmap3.draw("../output/density.html")



def compare_all_vs_one(verbose=0):

    os.chdir("../pickle_activity")
    df1 = pd.read_pickle("2019-04-09-08-29-05.pkl")  # all vs this one

    # 2018-12-20-16-42-55.pkl
    # 2019-03-12-08-32-49.pkl
    # 2018-11-29-18-09-16.pkl
    # 2019-03-18-17-25-10.pkl

    all_segments = []

    filename = "2019-03-25-17-24-10.pkl"

    #if 1:
    for filename in glob.glob("*.pkl"):

        if filename == "2019-04-09-08-29-05.pkl":
            continue

        df2 = pd.read_pickle(filename)
        if verbose:
            print(filename)

        gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)

        c1 = np.array(df1[["position_lat", "position_long"]]).T
        c2 = np.array(df2[["position_lat", "position_long"]]).T

        gmap3.plot(c1[0, :], c1[1, :], 'cornflowerblue', edge_width=2.5)
        gmap3.plot(c2[0, :], c2[1, :], 'green', edge_width=2.5)

        # Traitment...
        segments = extract_segment(c1, c2)
        if verbose:
            print("Number of segment found      :", len(segments))
            print("Segment length               :", [i.shape[1] for i in segments])

        # drop segments shorter than 20
        segments_filtered = [i for i in segments if i.shape[1] > 20]

        all_segments.extend(segments_filtered)

        if verbose:
            print("Number of filtered segment   :", len(segments_filtered))
            print("Filtered segment length      :", [i.shape[1] for i in segments_filtered])

        # Plot segment
        for segment in segments_filtered:
            # gmap3.plot(c1[0,array], c1[1,array], 'red', edge_width=4)
            gmap3.plot(segment[0, :], segment[1, :], 'red', edge_width=4)

        gmap3.draw("../output/" + filename + ".html")





    # c1 = np.array(df1[["position_lat", "position_long"]]).T
    # gmap3.plot(c1[0, :], c1[1, :], 'cornflowerblue', edge_width=2.5)
    # print(all_segments[0].shape)
    #
    # match = extract_segment(c1, all_segments[0])
    # #process_segments(all_segments)
    #
    # for segment in match:
    #     gmap3.plot(segment[0, :], segment[1, :], 'red', edge_width=4)
    #
    # gmap3.draw("../output/" + "match" + ".html")


# def process_segments(all_segments):
#
#     # Plot all segment
#     gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
#     for mean_trace in all_segments:
#         gmap3.plot(mean_trace[0, :], mean_trace[1, :], 'red', edge_width=4)
#     gmap3.draw("../output/" + "all_segments" + ".html")
#
#     print("Total number of segment         :", len(all_segments))
#
#     while(True):
#
#         remaining_seg = []
#
#         for segment_1 in all_segments:
#             for segment_2 in all_segments:
#                 if np.array_equal(segment_1, segment_2):
#                     continue
#
#                 segments = extract_segment(segment_1, segment_2)
#                 #if len(segments) > 0:
#                 #    print("add", len(segments), "segments")
#                 segments_filtered = [i for i in segments if i.shape[1] > 20]
#                 remaining_seg.extend(segments_filtered)
#
#         [print(i.shape) for i in remaining_seg]
#
#         if len(remaining_seg) == len(all_segments):
#             break
#
#         print("Remaining segments               :", len(remaining_seg), "over", len(all_segments)**2)
#         all_segments = remaining_seg
#
#     print("idem potence")
#
#     gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
#     for mean_trace in all_segments:
#         gmap3.plot(mean_trace[0, :], mean_trace[1, :], 'red', edge_width=4)
#     gmap3.draw("../output/" + "remaining_segments" + ".html")


def extract_segment(c1, c2):

    SIZE = 10
    STEP = 5
    c1_matched_c2 = np.zeros(c1.shape[1])
    c2_matched_c1 = np.zeros(c2.shape[1])

    mean_trace = np.zeros(c1.shape)
    #print(mean_trace.shape)

    # print(c2.shape[1])

    for i2 in range(0, c2.shape[1] - SIZE, STEP):  # todo ehh not optimal for:for...
        # print(i2)

        for i1 in range(0, c1.shape[1] - SIZE, 1):

            dist2 = np.linalg.norm(c1[:, i1:i1 + SIZE] - c2[:, i2:i2 + SIZE])

            if dist2 <= 0.00089443:
                c1_matched_c2[i1:i1 + SIZE] += 1
                c2_matched_c1[i2:i2 + SIZE] += 1

                mean_trace[:, i1:i1 + SIZE] = (c1[:, i1:i1 + SIZE] + c2[:, i2:i2 + SIZE]) / 2

    """segment extractor (list of segment)"""
    where = np.where(c1_matched_c2 > 1)[0]  # change the "> x" for different robustness (bigger = robust , but split big segment into smaller)
    # print("where:", where.shape)

    # print(where)
    # plt.scatter(where,where)
    # plt.show()
    diff = np.diff(where) > 1  # 1 if perfectly contigus
    # print("diff:",diff)
    if (diff == False).all():
        splitted = [where]

    else:
        sep = np.argwhere(diff).T[0]
        # print("separator:", sep)
        splitted = np.split(where, sep + 1)
        # print("splitted:", splitted)


    # ret= []
    # for i in splitted:
    #     print("i",i)
    #     ret.append(mean_trace[:, i])

    ret = [mean_trace[:, i] for i in splitted]

    return ret


def main():

    os.chdir("activity")

    """parse all fit file to pickle file and plot all on one map"""
    parse_all_to_pickle(False)

    density_map()

    #compare_all_vs_one()


if __name__ == "__main__":
    # execute only if run as a script
    main()
