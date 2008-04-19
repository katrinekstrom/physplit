#!/usr/bin/python

import os
global PYLIB_PATH
# pylib_path = os.path.join('home','tchubb','Uni-Files','pylib','')
PYLIB_PATH = '/home/tchubb/pylib/'

import sys
sys.path.append(PYLIB_PATH)
# modules
import numpy as n
import pylab as p
import hconf, harch, hexec, hplot, hdiag, htools
import mydatetime.mydatetime as cal

global HYMODELT_PATH, OUTFILE_ARCHIVE, METFILE_ARCHIVE
HYMODELT_PATH = PYLIB_PATH + '/hysplit4/exec/hymodelt'
OUTFILE_ARCHIVE =  '/home/tchubb/hysplit-output/GDAS/type-2/'
METFILE_ARCHIVE = '/home/tchubb/hysplit-data/'

def doit(date_list,return_traj=False,plot_traj=False):

    global HYMODELT_PATH, OUTFILE_ARCHIVE, METFILE_ARCHIVE, PYLIB_PATH
    
    trajectories=[]

    endpts=hconf.GenEndpts()
    for date in date_list:
	traj,flag=MakeTraj(endpts,[date],return_trajectories=True)
	trajectories.extend(traj)
	if flag:
	    print "ARGH!!!!!!!"
	    return [],1
	elif plot_traj:
	    PlotTraj(trajectories)

    if return_traj:
	return trajectories,0
    else:
	return [],0

def MakePlume(sources,date_list,\
	pollutant_data=None,\
	grid_data=None,\
	deposition_data=None):

    global HYMODELT_PATH, OUTFILE_ARCHIVE, METFILE_ARCHIVE, PYLIB_PATH

    infile  = PYLIB_PATH + 'physplit/working/conc-infile'
    outfile = 'conc-outfile'
    outfile_dir = PYLIB_PATH + 'physplit/working/'
    date_str=cal.FormatDate(date_list)
    dataset_dir=METFILE_ARCHIVE+'gdas/'

    plume_sources=[[ -38.273, 146.392, 50.0],
		    [-37.814, 144.963, 50.0],
		    [-33.186, 138.017, 50.0],
		    [-34.929, 138.601, 50.0]]

    k=-1
    for date in date_list:
	k+=1
	traj_archive_name = str(date_list[k]) + '-bt.dat'

	flag = hconf.WriteConcInfile(infile,\
		pollutant_data=pollutant_data,\
		grid_data=grid_data,\
		deposition_data=deposition_data,\
		conc_sourcepts=plume_sources,\
		run_time=96,\
		date=date,\
		dataset_dir=dataset_dir,\
		dataset_name=['gdas1.jul06.w4','gdas1.jul06.w5'],\
		outfile_dir=outfile_dir)



def MakeTraj(endpts,date_list,return_trajectories=False):

    global HYMODELT_PATH, OUTFILE_ARCHIVE, METFILE_ARCHIVE, PYLIB_PATH

    import csv
    infile  = PYLIB_PATH + 'physplit/working/hysplit-infile'
    outfile = 'hysplit-outfile'
    outfile_dir = PYLIB_PATH + 'physplit/working/'
    date_str=cal.FormatDate(date_list)
    dataset_dir=METFILE_ARCHIVE+'gdas/'

    dataset_files=hconf.select_GDAS_files(date_list,os.listdir(dataset_dir))
	    
    # sanity check
    for file in [infile.rstrip('/hysplit-infile'),outfile_dir]:
	try:
	    os.stat(file)
	except OSError:
	    print "physplit Error: ",file, " not found"
	    return [], 1

    k=-1
    for date in date_str: 
	# This loop contains all of the steps to create and archive trajectory output files. The 
	# creation and archiving are handled separately because it is too easy to overwrite precious  
	# files otherwise...
	
	k+=1
	traj_archive_name = str(date_list[k]) + '-bt.dat'

	flag = hconf.WriteTrajInfile(infile,
		    traj_endpts=endpts,
		    run_time=-96,
		    date=date,
		    dataset_dir=dataset_dir,
		    dataset_name=dataset_files,
		    outfile=outfile,
		    outfile_dir=outfile_dir)
    
	if flag:
	    print 'Error writing infile'
	    return [], 1
	
	# verify that there is a file at the designated path, fortran complains otherwise
	cmd = 'touch ' + outfile_dir + outfile
	os.system(cmd)
    
	# Call to hysplit:
	flag = hexec.ExecHymodelt(infile,hysplit_path=HYMODELT_PATH)
    
	if flag:
	    print 'failed to execute hysplit... check input files and paths'
	    return [], 1

	# Archive with interactive tool
	flags = harch.SaveTrajOutfile(outfile_dir+outfile,infile,archive_dir=OUTFILE_ARCHIVE,interactive=False)[0]
	if any(n.array(flags) == 'A'):
	    return [],1

    if return_trajectories:
	trajectories=harch.GetTrajectories(height=endpts[:,2],time_frame=date_list,archive_dir=OUTFILE_ARCHIVE)
	return trajectories, 0
    else:
	return [], 0

def PlotTraj(trajectories,plot_legend=True,plot_ground_tracks=True,plot_profiles=False):
    global PYLIB_PATH
    
    # trajectories=htools.SortTrajectories(trajectories,by_var='end_height')
    trajectories=htools.SortTrajectories(trajectories,by_var='end_date')

    map=hplot.SetDefaultBasemap(n.array([130,155]),n.array([-30,-45]) )
    # map=hplot.SetDefaultBasemap(n.array([130,156]),n.array([-30,-50]) )
    # map=hplot.SetDefaultBasemap(n.array([80,156]),n.array([-10,-70]) )

#    map=hplot.InvokeMap(coastfile=PYLIB_PATH+'physplit/plot_files/austcoast-small.dat',
#	    lllon=80,
#	    urlon=166,
#	    lllat=-55,
#	    urlat=0)


    if plot_ground_tracks:
        p.figure(1)
        p.clf()
        p.hold('on')
        hplot.PlotTrajectories(trajectories,map,[3,24],plot_legend=plot_legend)
        hplot.SetTitle(trajectories)
        hplot.PlotPollutionSources()
        map.drawmapboundary()
        map.drawcoastlines()
        map.drawmeridians(p.arange(90,161,10),labels=[1,0,0,1])
        map.drawparallels(p.arange(-60,0,10),labels=[1,0,0,0])
        # lims = hplot.SetCoordLim(map,80,166,-65,0)
        # p.axis(lims)
        # p.savefig(tmpfigs/)
	p.draw()

    if plot_profiles:
        p.figure(2)
	p.clf()
        hplot.VerticalProfiles(trajectories,[3,24])
        hplot.SetTitle(trajectories)
        p.grid('on')
        p.savefig(PYLIB_PATH+'/testing-2.png')
	p.xlabel('Parcel Age (hrs)')
	p.ylabel('Height (m AGL)')
    	p.draw()

    return None

def PlotConc(conc_outfile):

    lon,lat,conc_array=harch.ReadConcOutfile(conc_outfile)

    map=hplot.SetDefaultBasemap(n.array([125,165]),n.array([-25,-65]))

    p.figure()

    cont_levs=[n.power(10,i) for i in n.arange(-7,-13,-0.33)]
    cont_levs.reverse()

    rgb_tuples=hplot.ColorSpectrum(len(cont_levs))

    p.contourf(lon,lat,conc_array.T,cont_levs)

    map.drawcoastlines()
    map.drawmapboundary()
    map.drawmeridians(p.arange(90,161,10),labels=[1,0,0,1])
    map.drawparallels(p.arange(-60,0,10),labels=[1,0,0,0])

    p.title(conc_outfile)


