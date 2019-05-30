from src.race_manager import RaceManager
from src.race import Race

if __name__ == '__main__':

    # race_name = 'activity/2019-03-07-16-58-15.fit'
    #
    # race = Race(race_name)
    # race.parse_fit_file()
    # race.df_to_point_list()
    #
    # print(len(race.points))
    #
    # for i, point in enumerate(race.points):
    #     print(point)
    #     if i >= 20:
    #         break

    race_name = '2019-03-07-16-58-15'

    race_manager = RaceManager()
    # race_manager.read_all_races()
    # race_manager.save()
    race_manager = race_manager.load()
    race_manager.races[race_name].get_statistics()

    # for i, point in enumerate(race_manager.races[race_name].points):
    #     print(point)
    #     if i >= 20:
    #         break

    # for race in race_manager.races.values():
    #     print(len(race.points))

    # referential_race_name = "2019-04-09-08-29-05"  # All vs this one
    # race_manager.compare_all_vs_one(referential_race_name)
    # race_manager.save()
