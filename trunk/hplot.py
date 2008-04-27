#!/usr/bin/python
# from plot_files.PlotToolbox import *
"""Plot Trajectories to imitate procedures used in Matlab function of the same name"""
import numpy as n
import pylab as p
import matplotlib as m
from matplotlib.toolkits.basemap import Basemap
ar=n.array

def SetDefaultBasemap(lon=n.array([80,170]), lat=n.array([0,-65]), frame_width=5.):
    test = lon < 0.
    if True in test:
        # matplotlib expects 0-360 while WRF for example uses -180-180
        delta = n.ones(lon.shape)
        delta *= 360
        delta = ma.masked_where(lon > 0., delta)
        lon += delta.filled(fill_value=0)
    llcrnrlon=lon.min() - frame_width
    urcrnrlon=lon.max() + frame_width
    llcrnrlat=lat.min() - frame_width
    urcrnrlat=lat.max() + frame_width
    lon_0 = llcrnrlon + (urcrnrlon - llcrnrlon) / 2.
    lat_0 = llcrnrlat + (urcrnrlat - llcrnrlat) / 2.
        
    map = Basemap(
      llcrnrlon=llcrnrlon,
      llcrnrlat=llcrnrlat,
      urcrnrlon=urcrnrlon,
      urcrnrlat=urcrnrlat,
      resolution='l',
      projection='cyl',
      lon_0=lon_0,
      lat_0=lat_0
      )
    return map

def InvokeMap(coastfile='/media/sda4/map-data/aust-coast-noaa-2000000-1.dat',
		    lllon=80,
		    urlon=166,
		    lllat=-47,
		    urlat=-9,
		    draw_map=True):
    global PYLIB_PATH

    map = Basemap(projection='cyl',
			llcrnrlon=lllon,
			urcrnrlon=urlon,
			llcrnrlat=lllat,
			urcrnrlat=urlat,
			#lat_ts=-35,
			lat_0=-35,
			lon_0=120,
			resolution='l',
			area_thresh=1000.)


    try: 
	coast = p.load(coastfile)
	coast = p.load(coastfile)
	coast_x,coast_y = map(coast[:,0],coast[:,1])
	p.plot(coast_x,coast_y,color='black')    
    except IOError:
	map.drawcoastlines()

    map.drawmapboundary()
    map.drawmeridians(p.arange(0,360,10),labels=[0,0,1,0])
    map.drawparallels(p.arange(-90,0,10),labels=[1,0,0,0])

    return map

def SetCoordLim(map,lllon=80, urlon=166, lllat=-47, urlat=-9):

    "map coordinate limits to local axes return values"""

    lons = n.array([lllon,urlon])
    lats = n.array([lllat,urlat])

    X,Y = map(lons,lats)
    lims = [X[0],X[1],Y[0],Y[1]]

    return lims

def SetTitle(trajectories):

    hgt=[]
    endtime=[]

    for traj in trajectories:
	hgt.append(traj['endpoint'][2])
	endtime.append(traj['endtime'][-1])

    if len(n.unique(hgt))==1:
	p.title('Back Trajectories: ' + str(int(hgt[0]))+' m ')
    elif len(n.unique(endtime))==1:
	txt=trajectories[0]['endtime']
	p.title('Back Trajectories: ' + str(txt[2])+'/0'+str(txt[1])+'/0'+str(txt[0])+' '+str(txt[3]).zfill(2) + '00 UTC')

def PrintTrajEndtime(traj_endtime):

    text = str(traj_endtime[3]).zfill(2) + '00' + ' ' + str(traj_endtime[2]).zfill(2)+\
	    '/'+str(traj_endtime[1]).zfill(2)+'/'+str(traj_endtime[0]).zfill(2)

    return text


def SetLegendText(trajectories):

    same_endpoint=False
    same_endtime=False
    lgnd_txt=[]
    hgt=[]
    endtime=[]

    for traj in trajectories:
	hgt.append(traj['endpoint'][2])
	endtime.append(traj['endtime'][-1])

    if len(n.unique(hgt))==1:
	same_endpoint=True
    elif len(n.unique(endtime))==1:
	same_endtime=True

    for traj in trajectories:
	txt=traj['endtime'] 
	hgt=traj['endpoint'][2]

	if same_endtime:
	    # end height only in legend
	    next_text=str(str(int(hgt))) + 'm'
	elif same_endpoint:
	    # end time and date only in legend
	    # next_text = str(txt[3]).zfill(2) + '00' + ' ' +\
	    # 	str(txt[2]).zfill(2)+'/'+str(txt[1]).zfill(2)
	    next_text=PrintTrajEndtime(traj['endtime'])
	    # end time only in legend
	    # next_text = str(txt[3]).zfill(2) + '00' 
	else:
	    # all details in legend
	    next_text=str(txt[2])+'/0'+str(txt[1])+'/0'+str(txt[0])+\
		' '+str(txt[3]).zfill(2) + '00 ' + str(int(hgt)) + 'm'
		
	lgnd_txt.append(next_text)

    return lgnd_txt

def PlotPollutionSources():
    
    sources = n.array([[-38.2730, 146.3920], # Hazelwood
		[-37.8140, 144.9630], # Melbourne
		[-33.1860, 138.0170], # Port Pirie 
		[-34.9290, 138.6010]]) # Adelaide

    p.plot(sources[:,1],sources[:,0],'ro')



def PlotTrajectories(trajectories,map,time_increments=[3,12],plot_legend=True):
    
    num_trajs=trajectories.__len__()
    num_mrkrs=time_increments.__len__()
    num_pts   = trajectories[0]['age'].__len__() 
    clrs=ColorSpectrum(num_trajs)
    
    offset=[]
    for k in range(0,num_trajs) :
	for j in range(0,num_mrkrs):
	    offset.append( (trajectories[k]['endtime'][3])%(time_increments[j]))

    mrkr_sty=['.','^','o','s']
    plot_lines=[]
    end_times=[]

    for k in range(0,num_trajs):
	traj_x,traj_y=map(trajectories[k]['position'][:,1], trajectories[k]['position'][:,0] )
	next_line=p.plot(traj_x,traj_y,color=clrs[k])
	plot_lines.append(next_line)
	
	for j in range(num_mrkrs):
	    try:
    	        idx = range(offset[j+k*num_mrkrs],num_pts,time_increments[j])
    	        hndl = p.plot(traj_x[idx],traj_y[idx],'.')
    	        p.setp(hndl,marker=mrkr_sty[j],markerfacecolor=clrs[k])
	    except IndexError:
		pass

    if plot_legend:
	lgnd_txt=SetLegendText(trajectories)
	lgnd=p.legend(plot_lines,lgnd_txt, loc='lower right')
	texts = lgnd.get_texts()
	p.setp(texts, fontsize='small')


    # p.title(str(int(hgt))+' m ' + 'Back Trajectories: '+ str(txt[2])+'/0'+str(txt[1])+'/0'+str(txt[0])+' '+str(txt[3]).zfill(2) + '00 UTC')
    # p.title(str(int(hgt))+' m ' + 'Back Trajectories')


#    for k in range(0,num_trajs):
#	for j in range(0,num_mrkrs):
#	    idx = range(offset[j],num_pts,time_increments[j])
#	    hndl = p.plot(traj_x[idx],traj_y[idx],'.')
#	    print mrkr_sty[j]
#	    print clrs[k]
#	    p.setp(hndl,marker=mrkr_sty[j],markerfacecolor=clrs[k])


    return None

def VerticalProfiles(trajectories,time_increments=[3,12],plot_legend=True):

    num_trajs=trajectories.__len__()
    num_mrkrs=time_increments.__len__()
    num_pts   = trajectories[0]['age'].__len__() 
    clrs=ColorSpectrum(num_trajs)
    offset=[]

    for k in range(num_trajs) :
	for increment in time_increments:
	    offset.append( (trajectories[k]['endtime'][3])%(increment))

    mrkr_sty=['.','^','o','s']
    lgnd_txt=[]
    plot_lines=[]

    for k in range(0,num_trajs):
	age = trajectories[k]['age']
	height = trajectories[k]['position'][:,2] 
	next_line=p.plot(age,height,color=clrs[k])
	plot_lines.append(next_line)
	
	for j in range(num_mrkrs):
	    try:
    	        idx = range(offset[j+k*num_mrkrs],num_pts,time_increments[j])
    	        hndl = p.plot(age[idx],height[idx],'.')
    	        p.setp(hndl,marker=mrkr_sty[j],markerfacecolor=clrs[k])
	    except IndexError:
		pass

    if plot_legend:
	lgnd_txt=SetLegendText(trajectories)
	lgnd=p.legend(plot_lines,lgnd_txt, loc='upper right')
	texts = lgnd.get_texts()
	p.setp(texts, fontsize='small')

    # p.title('Back Trajectories: '+ str(txt[2])+'/0'+str(txt[1])+'/0'+str(txt[0])+' '+str(txt[3]).zfill(2) + '00 UTC')

    return None

def hue2clr(hue):
    """define a triplet based on the input hue, assuming saturation =1"""
    num = len(hue)

    #print 'hue=',hue
    #print 'hue.shape=',hue.shape

    rgb = n.zeros([hue.shape[0],3])

    #print 'rgb =', rgb


    for k in range(0,num):

	if (hue[k] >= 0) & (hue[k] < 0.167):

	    rgb[k,0] = 1
	    rgb[k,1] = hue[k]/0.167

	elif (hue[k]>= 0.167) & (hue[k] < 0.333):

	    rgb[k,0] = 1-(hue[k]-0.167)/0.167
	    rgb[k,1] = 1

	elif (hue[k] >= 0.333) & (hue[k] < 0.500):

	    rgb[k,1] = 1
	    rgb[k,2] = (hue[k]-0.333)/0.167

	elif (hue[k] >= 0.500) & (hue[k] < 0.667):

	    rgb[k,1] = 1-(hue[k]-0.500)/0.167
	    rgb[k,2] = 1

	elif (hue[k] >= 0.667) & (hue[k] < 0.883):

	    rgb[k,0] = (hue[k]-0.667)/0.167
	    rgb[k,2] = 1

	elif (hue[k] >= 0.883) & (hue[k] <= 1):

	    rgb[k,0] = 1
	    rgb[k,2] = 1-(hue[k]-0.883)/0.167

	#print 'k=',k
	#print 'rgb=',rgb
    return rgb
    

def ColorSpectrum(num_colors,return_as_tuples=False):
    """wrapper for the hue2clr module
    
    USAGE: ColorSpectrum(num_colors)
    OUTPUT: array of triplets defining equally 'spaced' colors on perimeter of color circle
    
    """
    if (num_colors == 1):
	hue=n.array([0])
    else:
	hue=p.frange(0,0.667,npts=num_colors)
	# print 'num_colors=',num_colors,'hue=',hue
    spect = hue2clr(hue)

    if return_as_tuples:
	rgb_tuple_list=[]
	for rgb_set in spect:
	    rgbtuple=(rgb_set[0],rgb_set[1],rgb_set[2])
	    rgb_tuple_list.append(rgbtuple)
	return rgb_tuple_list
    else:
	return spect



