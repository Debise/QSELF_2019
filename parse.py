from fitparse import FitFile
import os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import numpy as np
import gmplot 


def parse_it(filename):
    fitfile = FitFile(filename)
    fitfile.parse()

    records = list(fitfile.get_messages(name='record'))

    alt = []
    en_alt = []
    time = []
    heart = []
    speed = []
    cadence = []
    distance = []
    frac_cad = []
    x=[]
    y=[]
    for record in records:
        #print(field.name, field.value, field.units)
        alt.append(record.get('altitude').value / 10.0)
        en_alt.append(record.get('enhanced_altitude').value)
        heart.append(record.get('heart_rate').value)
        time.append(record.get('timestamp').value)
        speed.append(record.get('speed').value)
        cadence.append(record.get('cadence').value)
        distance.append(record.get('distance').value)
        frac_cad.append(record.get('fractional_cadence').value)

        x.append(record.get('position_lat').value)
        y.append(record.get('position_long').value)

    x = np.array(x)
    y = np.array(y)

    return x,y

def semi_to_degree(s):
    return s * (180.0 / 2**31)

#fitfile_path = os.path.join('2019-04-09-08-29-05.fit')
fitfile_1 = os.path.join('activity/2019-04-09-08-29-05.fit')
fitfile_2 = os.path.join('activity/2019-04-28-16-54-19.fit')

x1,y1 = parse_it(fitfile_1)
x2,y2 = parse_it(fitfile_2)



dx1 = semi_to_degree(x1)
dy1 = semi_to_degree(y1)
dx2 = semi_to_degree(x2)
dy2 = semi_to_degree(y2)

# for field in records[100]:
#     print(field.name, field.value, field.units)


# ax=plt.gca()
# xfmt = md.DateFormatter('%H:%M')
# ax.xaxis.set_major_formatter(xfmt)

# plt.subplot(6,1,1)
# plt.plot(time,alt)
# plt.plot(time,en_alt,c='r')
# plt.subplot(6,1,2)
# plt.plot(time,heart,c='r')
# plt.subplot(6,1,3)
# plt.plot(time,speed,c='r')
# plt.subplot(6,1,4)
# plt.plot(time,cadence,c='r')
# plt.subplot(6,1,5)
# plt.plot(time,frac_cad,c='r')
# plt.subplot(6,1,6)
# plt.plot(time,distance,c='g')

# plt.show()





# fig = plt.figure(figsize=(8, 8))
# m = Basemap(projection='lcc', resolution=None,
#             width=4E6, height=4E6, 
#             lat_0=45, lon_0=6,)
# m.etopo(scale=1, alpha=0.5)

# Map (long, lat) to (x, y) for plotting
# x, y = m(-122.3, 47.6)
# plt.plot(x, y, 'ok', markersize=5)
# plt.text(x, y, ' Seattle', fontsize=12);




gmap3 = gmplot.GoogleMapPlotter(45, 
                                6, 8) 
  
# scatter method of map object  
# scatter points on the google map 
gmap3.scatter( dx1, dy1, '# FF0000', 
                              size = 4, marker = False ) 
  
#Plot method Draw a line in 
#between given coordinates 
gmap3.plot(dx2, dy2,  
           'cornflowerblue', edge_width = 2.5) 
  
gmap3.draw( "map.html" ) 

# plt.plot(dx1,dy1,c="b")
# plt.plot(dx2,dy2,c="r")
# plt.show()

print("Nb point:",len(x1))
print("Nb point:",len(x2))
