#!/usr/bin/python

import os
global PYLIB_PATH
# pylib_path = os.path.join('home','tchubb','Uni-Files','pylib','')
PYLIB_PATH = '/home/tchubb/Uni-Files/pylib/'

import sys
sys.path.append(PYLIB_PATH)
# modules
import numpy as n
import pylab as p
import hconf, harch, hexec, hplot, hdiag, htools
import mydatetime.mydatetime as cal

global HYMODELT_PATH, OUTFILE_ARCHIVE, METFILE_ARCHIVE
HYMODELT_PATH = PYLIB_PATH + 'hysplit4/exec/hymodelt'
# OUTFILE_ARCHIVE = PYLIB_PATH + 'back_trajectories/testing/'
OUTFILE_ARCHIVE =  '/media/sda4/back-trajectories-data/testing/'

def doit(arch_prefix='testing/',return_traj=False):

    global HYMODELT_PATH, OUTFILE_ARCHIVE, METFILE_ARCHIVE
    # OUTFILE_ARCHIVE+=arch_prefix
    
    date_list=[2006073012, 2006073100]

    endpts=hconf.GenEndpts()
    for date in date_list:
	trajectories=MakeTraj(endpts,[date],return_trajectories=True)
	PlotTraj(trajectories)

    if return_traj:
	return trajectories


def MakeTraj(endpts,date_list,return_trajectories=False):

    global HYMODELT_PATH, OUTFILE_ARCHIVE, METFILE_ARCHIVE, PYLIB_PATH

    infile  = PYLIB_PATH + 'physplit/working/hysplit-infile'
    outfile = 'hysplit-outfile'
    outfile_dir = PYLIB_PATH + 'physplit/working/'
    date_str=cal.FormatDate(date_list)
	
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
		    dataset_dir='/media/sda4/hysplit-data/gdas/',
		    dataset_name=['gdas1.jul06.w4','gdas1.jul06.w5'],
		    outfile=outfile,
		    outfile_dir=outfile_dir)
    
	if flag:
	    print 'Error writing infile'
	    return 1
	
	# verify that there is a file at the designated path, fortran complains otherwise
	cmd = 'touch ' + outfile_dir + outfile
	os.system(cmd)
    
	# Call to hysplit:
	flag = hexec.exec_hymodelt(infile,hysplit_path=HYMODELT_PATH)
    
	if flag:
	    print 'failed to execute hysplit... check input files and paths'
	    return 1

	# Archive with interactive tool
	flags = harch.SaveTrajOutfile(outfile_dir+outfile,infile,archive_dir=OUTFILE_ARCHIVE,interactive=True)[0]
	if any(n.array(flags) == 'A'):
	    return None

    if return_trajectories:
	trajectories=harch.GetTrajectories(height=endpts[:,2],time_frame=date_list,archive_dir=OUTFILE_ARCHIVE)
	return trajectories
    else:
	return None

def PlotTraj(trajectories):
    
    trajectories=htools.SortTrajectories(trajectories,by_var='end_height')
    map=hplot.InvokeMap(lllon=80,
	    urlon=166,
	    lllat=-47,
	    urlat=-9)

    p.figure(1)
    # p.clf()
    hplot.PlotTrajectories(trajectories,map,[3,12,24],plot_legend=False)
    map.drawmapboundary
    lims = hplot.SetCoordLim(map,80,166,-47,-9)
    p.axis(lims)
    p.figure(2)
    hplot.VerticalProfiles(trajectories)
    p.show()

   
## Obsolete main scripts...


#def doit1(DATE):
#
#    plot_trajs=True
#
#    endpts = hconf.GenEndpts()
#
#    for k in range(0,DATE.__len__()):
#    
#	OUTFILE_PATH = '../test-data/'
#	TEST_OUTFILE = 'TEST_OUTFILE' 
#	TEST_INFILE  = '../test-data/TEST_INFILE'
#
#	Err_Flag = hconf.WriteTrajInfile(TEST_INFILE,
#		    traj_endpts=endpts,
#		    run_time=-96,
#		    date=DATE[k],
#		    outfile=TEST_OUTFILE,
#		    dataset_name=['gdas1.jul06.w4','gdas1.jul06.w5'],
#		    # dataset_name='gdas1.jul06.w4',
#		    outfile_dir=OUTFILE_PATH)
#    
#	if Err_Flag:
#	    print 'Error writing infile'
#	    return 1
#
#	cmd = 'touch ' + OUTFILE_PATH + TEST_OUTFILE
#	os.system(cmd)
#    
#	Err_Flag =  hexec.ExecHymodelt(TEST_INFILE,hysplit_path='../hysplit4/exec/hymodelt')
#    
#	if Err_Flag:
#	    print 'failed to execute hysplit... check input files and paths'
#	    return True
#
#	flags = AC.SaveTrajOutfile(OUTFILE_PATH+TEST_OUTFILE,TEST_INFILE,interactive=0)[0]
##	print flags
#	if any(n.array(flags) == 'A'):
#	    break
#
#    if not plot_trajs: 
#	return None
#    
#    trajectories=AT.SortTrajectories(trajectories)
#    map=PT.InvokeMap(lllon=80,
#	    urlon=166,
#	    lllat=-47,
#	    urlat=-9)
#
#    p.figure(1)
#    p.clf()
#    PT.PlotTrajectories(trajectories,map,[3,12,24])
#    map.drawmapboundary
#    lims = PT.SetCoordLim(map,80,166,-47,-9)
#    p.axis(lims)
#    p.figure(2)
#    PT.VerticalProfiles(trajectories)
#    p.show()
#
#    return None
#
#def doit2():
#
#    plot_trajs=True
#
#    end_times = AC.DateItr(6073100,6080100,3)
#    print 'end_times:', end_times
#
#    trajectories=AC.GetTrajectories(height=[1000.],time_frame=end_times )
#
##    H.WriteTrajOutfile(trajectories,trajfile='../test-data/regen_outfile')
#
#    if not plot_trajs: 
#	return None
#
#    p.close('all')
#    
#    trajectories=AT.SortTrajectories(trajectories)
#    map=PT.InvokeMap(lllon=80,
#	    urlon=166,
#	    lllat=-47,
#	    urlat=-9,
#	    draw_map=False)
#    p.figure(1)
#    PT.PlotTrajectories(trajectories,map,[6,24])
#    map.drawmapboundary
#    lims = PT.SetCoordLim(map,80,166,-47,-9)
#    p.axis(lims)
##    p.figure(2)
##    PT.VerticalProfiles(trajectories)
#    p.show()
#
#    return None
#
#def doitconc():
#
#    import EmissionCharacteristics as EC
#
#    plot_conc=False
#
#    G = EC.DefineLocalGrid(1)
#    P,D = EC.CreateEmissionsDictionary(1)
#    H.WriteConcInfile('../test-data/CONC_INFILE',P,G,D)
#
#    if not plot_conc: 
#	return None
#
#    p.close('all')
#    
#    trajectories=AT.SortTrajectories(trajectories)
#    map=PT.InvokeMap(lllon=80,
#	    urlon=166,
#	    lllat=-47,
#	    urlat=-9,
#	    draw_map=True)
#    p.figure(1)
#    PT.PlotTrajectories(trajectories,map,[3,12,24])
#    map.drawmapboundary
#    lims = PT.SetCoordLim(map,80,166,-47,-9)
#    p.axis(lims)
#    p.figure(2)
#    PT.VerticalProfiles(trajectories)
#    p.show()
#
#    return None
#
