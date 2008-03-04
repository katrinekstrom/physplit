#!/usr/bin/python
"""Suite to control hysplit inputs

Copyright (C) Thomas Chubb 2007
"""

import pylab as p
import numpy as n

def ExecHysplit_Traj(infile='../test-data/TEST_INFILE',
		    hysplit_path='/home/tchubb/hysplit4/exec/hymodelt'):

    """define a shell command and execute to operate hysplit"""
    import os
    import sys

    command = 'cat %s | %s' % (infile,hysplit_path)
    print command
    
    # Check infile location and try alternative defaults
    print 'Checking for infile %s...' % (infile)
    try:
	foo = os.stat(infile)
    except OSError:
	infile = '../test-data/TEST_INFILE'
	print 'Checking for infile %s...' % (infile)
	try:
	    foo = os.stat(infile)
	except OSError:
	    print 'Unable to locate infile... exiting'
	    return True

    # Check hyslpit path and try alternative defaults
    print 'Checking hysplit path %s...' % (hysplit_path)
    try:
	foo = os.stat(hysplit_path)
    except OSError:
	hysplit_path = '../hysplit4/exec/hymodelt'
	print 'Checking hysplit path %s...' % (hysplit_path)
	try:
	    foo = os.stat(hysplit_path)
	except OSError:
	    print 'Unable to locate hysplit... exiting'
	    return True
    
    command = 'cat %s | %s' % (infile,hysplit_path)
    print command

    os.system(command)
    
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
    import ArrayToolbox as AT
    # determine total number of trajectories to be requested
    if (len(traj_endpts.shape)==1):
	num_trajs=1
    else:
	# Sort list by end height and delete replicate trajectories
	traj_endpts=AT.unique2d(traj_endpts)
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

def ReadTrajOutfile(trajfile='default',header_only=False):
    """ Read the data in the hysplit output trajectory file and return as a data structure"""
    from sys import stdin
    from ArrayToolbox import strl2numl

    if trajfile == 'default':
	trajfile = '/media/sda4/back-trajectories-data/GDAS/0607312100-96-bt.dat'

    fid=open(trajfile)
    trajectories=[]

    str_cnts=fid.readline().split()
    num_grids=int(str_cnts[0])

    try: format_id=int(str_cnts[1])
    except ValueError: pass

    # There is some info in the header about the datasets used to generate the trajectories. These 
    # are ignored for the time being.
    for k in range(0,num_grids):
	fid.readline()
	# str_cnts=fid.readline().split()
	

    str_cnts=fid.readline().split()
    num_trajs=int(str_cnts[0])

    a={}

    for k in range(0,num_trajs):
	str_cnts=fid.readline().split()
	
	trajectories.append(a.copy())
	trajectories[k]['endtime']	= strl2numl(str_cnts[0:4])
	trajectories[k]['endpoint']	= strl2numl(str_cnts[4:],format='float')

    
    str_cnts=fid.readline().split()
    num_fields=int(str_cnts[0])
    
    for k in range(0,num_trajs):
	trajectories[k]['userfields'] = str_cnts[1:]

    # return here if only header info is required
    if header_only:
	trajectories_header=trajectories
	return trajectories_header
    
    # Read ALL of the remaining data
    data = fid.readlines()

    # d=data[:].split()

    num_lines=len(data)
    num_points=num_lines/num_trajs

    # preallocate memory for efficiency
    for k in range(0,num_trajs):
	trajectories[k]['timestamp']	= n.zeros([num_points,5])
	trajectories[k]['age']		= n.zeros([num_points,1])
	trajectories[k]['position']	= n.zeros([num_points,3])
	trajectories[k]['userdata']	= n.zeros([num_points,num_fields])

    for k in range(0,num_lines):
	# print 'k=',k
	d=data[k].split()
	traj_num=int(d[0])
	point_num=k/num_trajs

	# newitem=n.array( strl2numl(d[13:],'float')  )
	# print 'newitem=',newitem
	# print 'olditem=',trajectories[traj_num-1]['userdata'][point_num]

#	print d[0:2]
#	print d[2:7]
	trajectories[traj_num-1]['timestamp'][point_num]= n.array( strl2numl(d[2:7])  )
#	print [d[8]]
	trajectories[traj_num-1]['age'][point_num]	= n.array( strl2numl([d[8]],'float')  )
#	print d[9:12]
	trajectories[traj_num-1]['position'][point_num] = n.array( strl2numl(d[9:12],'float')  )
#	print d[12:]
	trajectories[traj_num-1]['userdata'][point_num] = n.array( strl2numl(d[12:],'float')  )

    return trajectories

def WriteTrajOutfile(trajectories,trajfile):
    """ToDo: Inverse function of ReadTrajOutfile, for completeness. Really boring!"""
    
    from sys import stdin
    fid=open(trajfile,'w')
    num_trajs=trajectories.__len__()

    print >>fid, 3, '# # #'
    print >>fid, 'This is a back trajectory database file generated by Python, NOT original hysplit output.'
    print >>fid, 'Only trajectory point locations are recorded by this file, other parameters are ignored.'
    print >>fid, 'hysplit-interface ((C) Thomas Chubb) will read this file exactly as if it were hysplit output.'

    print >>fid, num_trajs, '########', '#####'

    for k in range(0,num_trajs):
	pstr = str(trajectories[k]['endtime'][0])
	for m in range(1,trajectories[k]['endtime'].__len__()):
	    pstr += '\t' + str(trajectories[k]['endtime'][m]) 
	for m in range(0,trajectories[k]['endpoint'].__len__()):
	    pstr += '\t' + str(trajectories[k]['endpoint'][m]) 
	print >>fid, pstr

    pstr = str(trajectories[0]['userfields'].__len__())

    for m in range(0,trajectories[k]['userfields'].__len__()):
	pstr += '\t' + str(trajectories[k]['userfields'][m]) 

    print >>fid, pstr


    num_lines=trajectories[0]['age'].__len__()

    for j in range(0,num_lines):
	for k in range(0,num_trajs):
	    pstr = str(k+1) + '\t' + '#' 
	    for m in range(0,trajectories[k]['timestamp'][j].__len__()):
		pstr += '\t' + str(int(trajectories[k]['timestamp'][j][m])) 
	    pstr += '\t' + str(j)
	    for m in range(0,trajectories[k]['age'][j].__len__()):
		pstr += '\t' + str(trajectories[k]['age'][j][m]) 
	    for m in range(0,trajectories[k]['position'][j].__len__()):
		pstr += '\t' + str(trajectories[k]['position'][j][m]) 
	    for m in range(0,trajectories[k]['userdata'][j].__len__()):
		pstr += '\t' + str(trajectories[k]['userdata'][j][m]) 
	    print >>fid, pstr

    fid.close()

    return None

