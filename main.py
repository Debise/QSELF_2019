from src.race_manager import RaceManager
from src.race_inferer import RaceInferer
from src.race import Race

if __name__ == '__main__':

    process_all_race = 1
    infer_all = 1

    #####

    race_manager = RaceManager()

    """Processing all races take more than 25 minutes !"""
    if process_all_race:

        race_manager.read_all_races()
        # race_manager.save()
        # race_manager = race_manager.load()

        for race_name in race_manager.races:
            print(race_name)
            race_manager.compare_all_vs_one(race_name)
            race_manager.segment_density(race_name)
            race_manager.race_vs_segments(race_name)

        race_manager.save()

    else:
        race_manager = race_manager.load()

    #####

    race_inferer = RaceInferer()

    """Inferring the best segment of all race take more than """
    if infer_all:

        for race_name in race_inferer.race_manager.races:
            print(race_name)

            race_inferer.find_race_deniv(race_name)
            race_inferer.draw_denivelation_segment(race_name)

            race_inferer.find_race_density(race_name)
            race_inferer.draw_density_segment(race_name)

            race_inferer.find_race_length(race_name)
            race_inferer.draw_length_segment(race_name)

        race_inferer.save()

    else:
        race_inferer = race_inferer.load()

    
    ref_race = "2018-12-20-16-42-55" 

    print(race_inferer.get_statistics_from_deniv_seg(ref_race))

    # Test the "inference"

    print("Found", len(race_inferer.deniv_segment[ref_race]), "races matching the best deniv segment of ref race :", ref_race)
    print("Found", len(race_inferer.density_segment[ref_race]), "races matching the best density segment of ref race :", ref_race)
    print("Found", len(race_inferer.length_segment[ref_race]), "races matching the best length segment of ref race :", ref_race)


