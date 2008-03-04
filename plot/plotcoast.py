from numpy import *
from matplotlib import *
from matplotlib.toolkits.basemap import Basemap
import pylab as p

def doit():
    map = Basemap(projection='lcc',
		    llcrnrlon=80,
		    urcrnrlon=160,
		    llcrnrlat=-50,
		    urcrnrlat=-8,
		    #lat_ts=-35,
		    lat_0=-35,
		    lon_0=120,
		    resolution='c',
		    area_thresh=1000.)
    p.clf()
    map.drawcoastlines()
    # map.drawcountries()
    
    # map.drawrivers()

    map.drawmeridians(p.arange(0,360,10),labels=[0,0,1,0])
    map.drawparallels(p.arange(-90,0,10),labels=[1,0,0,0])

    traj=p.load('example_traj.dat')
    coast=p.load('/media/sda4/map-data/aust-coast-noaa-2000000-1.dat')

    traj_x,traj_y   = map(traj[:,1],traj[:,0]) 
    # coast_x,coast_y = map(coast[:,0],coast[:,1])
    
    p.plot(traj_x,traj_y)    
    p.plot(coast_x,coast_y,color='black')    

    map.drawmapboundary()
    p.show()
    return map 
