#!/usr/bin/python
"""Suite to configure hysplit inputs

This module is a set of functions to control all of the read/write to 
the namelist files for hysplit.

Copyright (C) Thomas Chubb 2008
"""

import numpy as n



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

def WriteTrajInfile(infile,date='06 07 28 00',
		    	# num_trajs=1,
			traj_endpts=n.array([-36.3869, 148.394, 1000]),
			run_time=-96,
			vert_mode=0,
			model_top=10000,
			# num_datasets=1,
			dataset_dir='/media/sda4/hysplit-data/',
			dataset_name='gdas1.jul06.w4',
			outfile_dir='/media/sda4/hysplit-dump/',
			outfile='outfile-traj' ):


    """function to open and edit hymodelt input file
    
    USAGE:
    ** keyword args
	- date: YY MM DD HH ['06 07 28 00']
	- num_trajs: [1]
	- traj_endpt: lat lon ht [array([-36.3869 148.394 1000])]
	- run_time: [-96]
	- vert_mode: [0]
	- model_top: [10000]
	- num_datasets: [1]
	- dataset_dir: ['/media/sda4/hysplit-data/']
	- dataset_name: ['gdas1.jul06.w4']
	- outfile_dir: ['/media/sda4/hysplit-dump/']
	- outfile_name: ['outfile']
    
    COMMENTS
    At this stage only one trajectory endpoint is specified, as the code 
    is currently being developed for use in back trajectory analysis. This
    will most likely be improved upon at a later date.
    """
    import htools as tools
    # determine total number of trajectories to be requested
    if (len(traj_endpts.shape)==1):
	num_trajs=1
    else:
	# Sort list by end height and delete replicate trajectories
	traj_endpts=tools.unique2d(traj_endpts)
	num_trajs=traj_endpts.shape[0]

    # dataset_name may be a string (not iterable) or a list or an array
    if hasattr(dataset_name,'__iter__'):
	num_datasets=dataset_name.__len__()
    else:
	num_datasets=1
    
    # same with dataset_dir
    if hasattr(dataset_dir,'__iter__'):
	num_dataset_dirs=dataset_dir.__len__()
	# now, this must be 1 or match the number of datasets
	if ((num_dataset_dirs != num_datasets) and (num_dataset_dirs != 1)):
	    print '>>> Error: Specify one dataset directory OR exactly one directory per dataset!'
	    return 1
    else:
	num_dataset_dirs=1

    # open file for write access
    fid=open(infile,'w')
    
    print >>fid,date
    print >>fid,num_trajs

    for k in range(0,num_trajs):
	# print "k=", k
	# print "traj_endpts=",traj_endpts[k]
	# print "num_trajs=",num_trajs
	if (num_trajs==1):
	    print >>fid, '%3.4f %3.4f %3.0f' % (traj_endpts[0], traj_endpts[1], traj_endpts[2]) 
	else:
	    print >>fid, '%3.4f %3.4f %3.0f' % (traj_endpts[k,0], traj_endpts[k,1], traj_endpts[k,2]) 
    
    print >>fid,run_time
    print >>fid,vert_mode
    print >>fid,model_top
    print >>fid,num_datasets

    for k in range(0,num_datasets):
	if (num_dataset_dirs==1):
	    print >>fid,dataset_dir
	else:
	    print >>fid,dataset_dir[k]
	
	print >>fid,dataset_name[k]

    print >>fid,outfile_dir
    print >>fid,outfile

    fid.close
    return None

def WriteConcInfile(infile,pollutant,grid,deposition,
			date='06 07 28 00',
			conc_sourcepts=n.array([-33.1858, 138.0169, 50.0]),
			run_time=48,
			vert_mode=0,
			model_top=10000,
			# num_datasets=1,
			dataset_dir=['/media/sda4/hysplit-data/'],
			dataset_name=['gdas1.jul06.w4'],
			outfile_dir=['/media/sda4/hysplit-dump/'],
			outfile=['outfile-conc'] ):

    """function to open and edit hymodelc input file"""
     
    # determine total number of sources to be requested
    if (len(conc_sourcepts.shape)==1):
	num_sources=1
    else:
	num_sources=conc_sourcepts.shape[0]

    # dataset_name may be a string (not iterable) or a list or an array
    if hasattr(dataset_name,'__iter__'):
	num_datasets=dataset_name.__len__()
    else:
	num_datasets=1
    
    # same with dataset_dir
    if hasattr(dataset_dir,'__iter__'):
	num_dataset_dirs=dataset_dir.__len__()
	# now, this must be 1 or match the number of datasets
	if ((num_dataset_dirs != num_datasets) and (num_dataset_dirs != 1)):
	    print '>>> Error: Specify one dataset directory OR exactly one directory per dataset!'
	    return 1
    else:
	num_dataset_dirs=1

    num_pollutants=pollutant.__len__()
    num_grids=grids.__len__()

    # open file for write access
    fid=open(infile,'w')
    
    print >>fid,date
    print >>fid,num_sources

    for k in range(0,num_sources):
	# print "k=", k
	# print "conc_sourcepts=",conc_sourcepts[k]
	# print "num_sources=",num_sources
	if (num_sources==1):
	    print >>fid, '%3.4f %3.4f %3.0f' % (conc_sourcepts[0], conc_sourcepts[1], conc_sourcepts[2]) 
	else:
	    print >>fid, '%3.4f %3.4f %3.0f' % (conc_sourcepts[k,0], conc_sourcepts[k,1], conc_sourcepts[k,2]) 
    
    print >>fid,run_time
    print >>fid,vert_mode
    print >>fid,model_top
    print >>fid,num_datasets

    for k in range(0,num_datasets):
	if (num_dataset_dirs==1):
	    print >>fid,dataset_dir
	else:
	    print >>fid,dataset_dir[k]
	
	print >>fid,dataset_name



    print >>fid,outfile_dir
    print >>fid,outfile

    fid.close
    return None

