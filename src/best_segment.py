import numpy as np
from src.segment_comparator import SegmentComparator
import settings as st
from gmplot import GoogleMapPlotter
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


class BestSegment:

    def __init__(self, referential_race_name, all_segments, mean_seg_density):
        self.referential_race_name = referential_race_name
        self.all_segments = all_segments
        self.mean_seg_density = mean_seg_density

        self.deniv_segment = None
        self.density_segment = None
        self.length_segment = None

    def __str__(self):
        string = ""

        return string

    def get_length_segment(self):
        # all_segments.sort(key=lambda x: x[1].shape[1], reverse=True)  # tri par nb de point

        length_dict = dict()
        n = 0
        new_all_segments = []
        for seg in self.all_segments:
            segment = seg.positions

            dist_start = np.min(segment[3, :])
            dist_stop = np.max(segment[3, :])
            distance = dist_stop - dist_start
            # print(name, dist_start, dist_stop, distance)

            new_all_segments.append(("seg" + str(n), seg))

            # print("max diff", np.max(np.diff(segment[3,:])))

            length_dict["seg" + str(n)] = distance
            n += 1

        max_length_seg = max(length_dict, key=lambda k: length_dict[k])
        length_segment = [segment for (name, segment) in new_all_segments if name == max_length_seg][0]

        # print(">>", max_length_seg, length_dict[max_length_seg])

        # gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
        # gmap3.plot(length_segment[0, :], length_segment[1, :], 'red', edge_width=4)
        # gmap3.draw("../output/" + "length_segment" + ".html")

        self.length_segment = length_segment
        return length_segment

    def get_density_segment(self):

        new_all_segments = list(self.all_segments)

        # while(True):
        if 1:

            remaining_seg = []

            # for (name_1, segment_1) in all_segments:
            for i in range(len(self.all_segments) - 1):
                seg_1 = new_all_segments.pop(0)  # pour ne pas faire seg1 vs seg2, PUIS seg2 vs seg1
                segment_1 = seg_1.positions
                name_1 = seg_1.times1[0]  # selon convention dans RaceManager density
                # print(segment_1.shape)
                # print("aa:",i,len(all_segments))

                for seg_2 in new_all_segments:
                    segment_2 = seg_2.positions
                    name_2 = seg_2.times1[0]  # selon convention dans RaceManager density

                    if np.array_equal(segment_1, segment_2):
                        # ne pas faire si ils sont égaux
                        print("Egal pass", segment_1.shape, segment_2.shape)
                        continue

                    # print(self.mean_seg_density[name_1], self.mean_seg_density[name_2])
                    if self.mean_seg_density[name_1] < 0.5 or self.mean_seg_density[
                        name_2] < 0.5:  # si les deux densité sont plus grandes que...
                        # print("continue 1")
                        continue

                    segmentComparator = SegmentComparator(seg_1, seg_2)
                    segmentComparator.extract_segment()
                    segments = segmentComparator.segments  # Warning the timestamp given by SegmentComparator aren't very relevant!

                    # todo si seg1 & seg2 sont "semblables" --> 1 on garde le plus long, 2 on garde le plus court, 3  on garde que le match et delete les 2 primitive .......
                    # todo Solution 3 si l'on a un bout commun plus grand XX

                    # todo BUT trouver les chemin qui sont soit très long (>200) // soit ceux qui ont été fait + que 5 fois et suffisamment long // soit ceux avec le plus de deni ?????
                    # faire avec la densité (voisine) sur une bonne partie (80%) du chemin --> ___si > que 5 (course différente) sur 80% du segment _____par exemple (truc de la moyenne pour améliorer le segment)
                    # on peut pas tout faire --> indiquer les améliorations possibles

                    # todo utiliser LCSS ou autre pour retirer les segement trop similaire OU OU faire avec un kind of "extract segment"

                    # print(len(segments))
                    # [print(len(i.points1)) for i in segments if len(i.points1) > 50]

                    segments_filtered = [i for i in segments if len(i.points1) > 50]  # todo taille minimum

                    if len(segments_filtered) > 1:
                        print("it generates more segments -----------------------------------------",
                              len(segments_filtered))
                        continue

                    if len(segments_filtered) == 0:
                        # print(">>",segments_filtered)
                        # print("-------> LEN == 0")
                        continue

                    if segments_filtered[0].positions.shape[1] < 0.7 * segment_1.shape[1] and \
                            segments_filtered[0].positions.shape[1] < 0.7 * segment_2.shape[1]:
                        # si le résultat est plus court que 70% pour chacunes des deux origines
                        continue

                    # print(segments_filtered[0].positions.shape)

                    # add the run name with the segment to recover them later....
                    if self.mean_seg_density[name_1] < self.mean_seg_density[name_2]:
                        name = name_2
                    else:
                        name = name_1

                    # name = list(name_1)
                    # name.extend(list(name_2))
                    segments_with_run_name = [(name, i) for i in segments_filtered]
                    remaining_seg.extend(segments_with_run_name)

                    # todo ~~ garder les plus court avec le plus de densité...

            # print("Remaining segments               :", len(remaining_seg))

            # reprocessing on "new" remaining segment

            n = 0
            all_segments = []
            for (name, segment) in remaining_seg:
                all_segments.append(("seg" + str(n), segment))
                n += 1

            # print(len(all_segments))

            density, delta, mean_seg_density = self.density(all_segments)

            max_density_seg = max(mean_seg_density, key=lambda k: mean_seg_density[k])

            # print(max_density_seg)

            density_segment = [segment for (name, segment) in all_segments if name == max_density_seg][0]
            # print(density_segment.positions.shape)

        # gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
        # for (name, mean_trace) in all_segments:
        #     gmap3.plot(mean_trace[0, :], mean_trace[1, :], 'purple', edge_width=4)

        # gmap3.plot(density_segment[0, :], density_segment[1, :], 'red', edge_width=4)

        # gmap3.draw("../output/" + "density_segment" + ".html")

        self.density_segment = density_segment
        return density_segment

    def get_denivelation_segment(self):

        deniv_dict = dict()
        n = 0
        new_all_segments = []
        for seg in self.all_segments:
            segment = seg.positions

            # print(segment.shape)
            # print(segment[2, :])

            derivative = np.diff(segment[2, :])
            derivative[derivative < 0] = 0
            positive_deniv = np.sum(derivative)  # only positive !
            # print(name, positive_deniv)

            new_all_segments.append(("seg" + str(n), seg))

            deniv_dict["seg" + str(n)] = positive_deniv
            n += 1

        max_deniv_seg = max(deniv_dict, key=lambda k: deniv_dict[k])
        deniv_segment = [segment for (name, segment) in new_all_segments if name == max_deniv_seg][0]

        # print(">>",max_deniv_seg, deniv_dict[max_deniv_seg])

        # gmap3 = gmplot.GoogleMapPlotter(46.98, 6.89, 14)
        # gmap3.plot(deniv_segment[0, :], deniv_segment[1, :], 'red', edge_width=4)
        # gmap3.draw("../output/" + "deniv_segment" + ".html")

        self.deniv_segment = deniv_segment
        return deniv_segment

    def draw(self):
        if self.deniv_segment is None or self.length_segment is None or self.deniv_segment is None:
            print("Need to call all 3 get_..._segment before draw()")
            return -1

        gmap3 = GoogleMapPlotter(46.98, 6.89, 14, apikey=GOOGLE_MAP_API_KEY)

        self.length_segment.draw('purple', gmap3=gmap3)
        self.density_segment.draw('red', gmap3=gmap3)
        self.deniv_segment.draw('yellow', gmap3=gmap3)

        filename = os.path.join(st.files["output_folder"], f"best_segment_{self.referential_race_name}.html")
        gmap3.draw(filename)

        return 0

    @staticmethod
    def density(seg_list):

        # print(len(seg_list))
        # seg_list --> list de tuple (run_name, segment_array)

        points = np.array(seg_list[0][1].positions[:2, :])

        for segment in seg_list[1:]:
            if len(segment) != 2:
                print("passed")
                continue

            try:
                points = np.append(points, (segment.positions[:2, :]), axis=1)
            except:
                pass
                # print("Probably zero size array...")

        max_lat = np.max(points[0, :])
        max_long = np.max(points[1, :])
        min_lat = np.min(points[0, :])
        min_long = np.min(points[1, :])

        # print(min_lat, min_long, max_lat, max_long)

        # delta_lat = (max_lat - min_lat) / division_interval
        # delta_long = (max_long - min_long) / division_interval

        delta = 0.0005

        lat = np.arange(min_lat, max_lat, delta)
        long = np.arange(min_long, max_long, delta)

        # print(lat.shape)
        # print(long.shape)

        density = np.zeros([3, lat.shape[0] * long.shape[0]])  # [lat,long,nbpoint]
        # print(density.shape)

        i = 0
        for x in lat:
            for y in long:
                # parcours de la "grid"

                density[0, i] = x
                density[1, i] = y

                for (seg_name, segment) in seg_list:
                    seg = segment.positions

                    x_less = np.where(seg[0, :] >= (x - delta / 2))
                    x_more = np.where(seg[0, :] < (x + delta / 2))
                    count_x = np.intersect1d(x_less, x_more)

                    y_less = np.where(seg[1, :] >= (y - delta / 2))
                    y_more = np.where(seg[1, :] < (y + delta / 2))
                    count_y = np.intersect1d(y_less, y_more)

                    valid_coordinate = np.intersect1d(count_x, count_y).shape[0]

                    if valid_coordinate > 0:
                        # on ajoute 1 si le segment est dedans (la case de la grid)
                        density[2, i] = density[2, i] + 1

                i += 1

        # print("Max seg density :", np.max(density[2, :]))

        # todo repasser tous les segment et ajouter leur propre densité max pour chacun
        max_seg_density = dict()
        min_seg_density = dict()
        mean_seg_density = dict()
        seg_present_in = dict()
        for (seg_name, segment) in seg_list:
            seg = segment.positions

            min_seg_density[seg_name] = 100
            max_seg_density[seg_name] = 0
            mean_seg_density[seg_name] = 0
            seg_present_in[seg_name] = 0

        i = 0
        for x in lat:
            for y in long:
                # parcours de la "grid"

                for (seg_name, segment) in seg_list:
                    seg = segment.positions

                    x_less = np.where(seg[0, :] >= (x - delta / 2))
                    x_more = np.where(seg[0, :] < (x + delta / 2))
                    count_x = np.intersect1d(x_less, x_more)

                    y_less = np.where(seg[1, :] >= (y - delta / 2))
                    y_more = np.where(seg[1, :] < (y + delta / 2))
                    count_y = np.intersect1d(y_less, y_more)

                    valid_coordinate = np.intersect1d(count_x, count_y).shape[0]

                    if valid_coordinate > 0:
                        if density[2, i] > max_seg_density[seg_name]:
                            # si le segment est dedans (la case de la grid)
                            max_seg_density[seg_name] = density[2, i]

                        if density[2, i] < min_seg_density[seg_name]:
                            min_seg_density[seg_name] = density[2, i]

                        mean_seg_density[seg_name] += density[2, i]
                        seg_present_in[seg_name] += 1

                i += 1

        for (seg_name, seg) in seg_list:
            if seg_present_in[seg_name] == 0:
                mean_seg_density[seg_name] = 0
            else:
                mean_seg_density[seg_name] = mean_seg_density[seg_name] / seg_present_in[seg_name]

        # print(max_seg_density)
        # print(min_seg_density)
        # print(seg_present_in)
        # print(mean_seg_density)

        return density, delta, mean_seg_density
