from src.RaceManagerClass import RaceManager
from src.RaceClass import Race

if __name__ == '__main__':

    process_all_race = 1
    race_manager = RaceManager()

    """Processing all races take more than 15 minutes !"""
    if process_all_race:
        
        race_manager.read_all_races()
        # race_manager.save()
        #race_manager = race_manager.load()

        for race_name in race_manager.races:
            print(race_name)
            race_manager.compare_all_vs_one(race_name)
            race_manager.segment_density(race_name)
            race_manager.race_vs_segments(race_name)
            
        race_manager.save()
    
    else:
        race_manager = race_manager.load()

    

    # seg = race_manager.all_seg_of_one_race["2019-01-09-15-51-47"][0]
    # print(type(seg))
    # print(seg.positions.shape)
    # print(seg.positions)#contient lat,long,alt,dist


    # density test


    #####

    #for race_name in race_manager.races:
    #    print(race_name)

    #for race_name in race_manager.race_comparators:
    #    print(type(race_manager.race_comparators[race_name]))

    # for race_name in race_manager.all_seg_of_one_race:
    #    segment_list = race_manager.all_seg_of_one_race[race_name]
    #    print(race_name, "--> Nb seg:", len(segment_list))

        #segment_vs_run




    #race_manager.race_vs_segments("2018-12-20-16-42-55") 
