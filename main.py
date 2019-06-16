from src.race_manager import RaceManager
from src.race_inferer import RaceInferer
from src.race_inferer_wrapper import RaceInfererWrapper
from src.race import Race
from multiprocessing import cpu_count, Pool
import gmplot
import numpy as np


if __name__ == '__main__':

    process_all_race = 0
    infer_all = 0

    nb_thread = cpu_count()
    print(nb_thread, "CPUs available on this machine...")

    #####

    race_manager = RaceManager()
    number_of_races = 0

    """Processing all races take more than 25 minutes !"""
    if process_all_race:

        print("Process all races")

        race_manager.read_all_races()

        number_of_races = len(list(race_manager.races.keys()))
        i=0
        print("Number of races to process :", number_of_races)

        for race_name in race_manager.races:
            i += 1
            print(str(i) + "/" + str(number_of_races), ":", race_name)
            race_manager.compare_all_vs_one(race_name)
            race_manager.segment_density(race_name)
            race_manager.race_vs_segments(race_name)

        race_manager.save()

    #####

    """Inferring the best segment of all race take more than ... a lot """
    if infer_all:

        print("Infer all races")

        i = 0 
        race_inferer = RaceInferer()

        for race_name in race_inferer.race_manager.races:
            i += 1
            print(str(i) + "/" + str(number_of_races), ":", race_name)
            race_inferer.find_race_deniv(race_name)
            race_inferer.draw_denivelation_segment(race_name)

            race_inferer.find_race_density(race_name)
            race_inferer.draw_density_segment(race_name)

            race_inferer.find_race_length(race_name)
            race_inferer.draw_length_segment(race_name)

        race_inferer.save()
        

    #####
    
    
    #ref_race = "2018-12-20-16-42-55" 
    ref_race = "2019-03-25-17-24-10"

    race_inferer_wrapper = RaceInfererWrapper()

    # To get statistics of a best segment: 
    #print(race_inferer.get_statistics_from_deniv_seg(ref_race))

    # Check the "inference"
    deniv, length, density = race_inferer_wrapper.get_best_segment(ref_race)

    # print("Found", len(deniv), "races matching the best deniv segment of ref race :", ref_race)
    # print("These matching reaces are :", [race_name for (race_name, seg) in deniv])
    # print("Segment.type for best devi. seg. :", [seg.segment_type for (race_name, seg) in deniv])
    # print("")

    # print("Found", len(density), "races matching the best density segment of ref race :", ref_race)
    # print("These matching reaces are :", [race_name for (race_name, seg) in density])
    # print("Segment.type for best devi. seg. :", [seg.segment_type for (race_name, seg) in density])
    # print("")

    # print("Found", len(length), "races matching the best length segment of ref race :", ref_race)
    # print("These matching reaces are :", [race_name for (race_name, seg) in length])
    # print("Segment.type for best devi. seg. :", [seg.segment_type for (race_name, seg) in length])
    # print("")

#TODO print density map

    # race = race_inferer_wrapper.race_inferer.race_manager.races[ref_race]
    # density_table = race_inferer_wrapper.race_inferer.race_manager.race_segment_density[ref_race]
    # print(density_table.shape)

    # #density map
    # gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 13.6)

    # c = race.df[["timestamp", "position_lat", "position_long", "altitude", "distance"]].values.T
    # gmap3.plot(c[1, :], c[2, :], 'cornflowerblue', edge_width=2.5)

    # for i in range(density_table.shape[1]):
    #     if density_table[2, i] > 0:
    #         gmap3.scatter([density_table[0, i]], [density_table[1, i]], "yellow", size=np.sqrt(density_table[2, i]) * 8, marker=False)

    # gmap3.draw("rapport_density.html")

    # #density with segment density
    # gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 13.6)

    # c = race.df[["timestamp", "position_lat", "position_long", "altitude", "distance"]].values.T
    # gmap3.plot(c[1, :], c[2, :], 'cornflowerblue', edge_width=2.5)

    # for i in range(density_table.shape[1]):
    #     if density_table[2, i] > 0:
    #         gmap3.scatter([density_table[0, i]], [density_table[1, i]], "yellow", size=np.sqrt(density_table[2, i]) * 8, marker=False)

    # gmap3.plot(density[0][1].positions[0, :], density[0][1].positions[1, :], 'red', edge_width=5)

    # gmap3.draw("rapport_density_with_seg.html")

    # #segment length
    # gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 13.6)

    # c = race.df[["timestamp", "position_lat", "position_long", "altitude", "distance"]].values.T
    # gmap3.plot(c[1, :], c[2, :], 'cornflowerblue', edge_width=2.5)

    # gmap3.plot(length[0][1].positions[0, :], length[0][1].positions[1, :], 'red', edge_width=5)

    # gmap3.draw("seg_length.html")

    # #segment deniv
    # gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 13.6)

    # c = race.df[["timestamp", "position_lat", "position_long", "altitude", "distance"]].values.T
    # gmap3.plot(c[1, :], c[2, :], 'cornflowerblue', edge_width=2.5)

    # gmap3.plot(deniv[0][1].positions[0, :], deniv[0][1].positions[1, :], 'red', edge_width=5)

    # gmap3.draw("seg_denivh.html")



