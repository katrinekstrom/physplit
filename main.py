#!/usr/bin/python
import pylab as p
import numpy as n
import hconf, harch, hexec, hplot, hdiag
import os


def GenEndpts():
    """a set of endpoints, feel free to edit"""
    
    heights=n.array([])
    heights=n.append(heights,n.arange(1000,5000,500))
    heights=n.append(heights,n.arange(200,1000,200))
    heights=heights*n.ones([1,1])

    lats = n.ones(heights.shape)*-36.3869
    lons = n.ones(heights.shape)*148.394

    endpts =n.hstack((lats.T,lons.T,heights.T))
    return endpts


def dummy():
    return None


def doit1(DATE):

    plot_trajs=True

    endpts = GenEndpts()

    for k in range(0,DATE.__len__()):
    
	OUTFILE_PATH = '../test-data/'
	TEST_OUTFILE = 'TEST_OUTFILE' 
	TEST_INFILE  = '../test-data/TEST_INFILE'

	Err_Flag = H.WriteTrajInfile(TEST_INFILE,
		    traj_endpts=endpts,
		    run_time=-96,
		    date=DATE[k],
		    outfile=TEST_OUTFILE,
		    dataset_name=['gdas1.jul06.w4','gdas1.jul06.w5'],
		    # dataset_name='gdas1.jul06.w4',
		    outfile_dir=OUTFILE_PATH)
    
	if Err_Flag:
	    print 'Error writing infile'
	    return 1

	cmd = 'touch ' + OUTFILE_PATH + TEST_OUTFILE
	os.system(cmd)
    
	Err_Flag =  H.ExecHysplit_Traj(TEST_INFILE,hysplit_path='../hysplit4/exec/hymodelt')
    
	if Err_Flag:
	    print 'failed to execute hysplit... check input files and paths'
	    return True

	flags = AC.SaveTrajOutfile(OUTFILE_PATH+TEST_OUTFILE,TEST_INFILE,interactive=0)[0]
#	print flags
	if any(n.array(flags) == 'A'):
	    break

    if not plot_trajs: 
	return None
    
    trajectories=AT.SortTrajectories(trajectories)
    map=PT.InvokeMap(lllon=80,
	    urlon=166,
	    lllat=-47,
	    urlat=-9)

    p.figure(1)
    p.clf()
    PT.PlotTrajectories(trajectories,map,[3,12,24])
    map.drawmapboundary
    lims = PT.SetCoordLim(map,80,166,-47,-9)
    p.axis(lims)
    p.figure(2)
    PT.VerticalProfiles(trajectories)
    p.show()

    return None

def doit2():

    plot_trajs=True

    end_times = AC.DateItr(6073100,6080100,3)
    print 'end_times:', end_times

    trajectories=AC.GetTrajectories(height=[1000.],time_frame=end_times )

#    H.WriteTrajOutfile(trajectories,trajfile='../test-data/regen_outfile')

    if not plot_trajs: 
	return None

    p.close('all')
    
    trajectories=AT.SortTrajectories(trajectories)
    map=PT.InvokeMap(lllon=80,
	    urlon=166,
	    lllat=-47,
	    urlat=-9,
	    draw_map=False)
    p.figure(1)
    PT.PlotTrajectories(trajectories,map,[6,24])
    map.drawmapboundary
    lims = PT.SetCoordLim(map,80,166,-47,-9)
    p.axis(lims)
#    p.figure(2)
#    PT.VerticalProfiles(trajectories)
    p.show()

    return None

def doitconc():

    import EmissionCharacteristics as EC

    plot_conc=False

    G = EC.DefineLocalGrid(1)
    P,D = EC.CreateEmissionsDictionary(1)
    H.WriteConcInfile('../test-data/CONC_INFILE',P,G,D)

    if not plot_conc: 
	return None

    p.close('all')
    
    trajectories=AT.SortTrajectories(trajectories)
    map=PT.InvokeMap(lllon=80,
	    urlon=166,
	    lllat=-47,
	    urlat=-9,
	    draw_map=True)
    p.figure(1)
    PT.PlotTrajectories(trajectories,map,[3,12,24])
    map.drawmapboundary
    lims = PT.SetCoordLim(map,80,166,-47,-9)
    p.axis(lims)
    p.figure(2)
    PT.VerticalProfiles(trajectories)
    p.show()

    return None

