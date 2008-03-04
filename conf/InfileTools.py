#!/usr/bin/python
"""Suite to control hysplit inputs"""

from numpy import *

def WriteInfile(infile,date='06 07 28 00',
		    	num_trajs=1,
			traj_endpt=array([-36.3869, 148.394, 1000]),
			run_time=-96,
			vert_mode=0,
			model_top=10000,
			num_datasets=1,
			dataset_dir='~/data_drive/hysplit-data/',
			dataset_name='gdas1.jul06.w4',
			outfile_dir='~/media/sda4/hysplit-dump/',
			outfile_name='outfile' ):


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
	- dataset_dir: ['~/data_drive/hysplit-data/']
	- dataset_name: ['gdas1.jul06.w4']
	- outfile_dir: ['~/data_drive/hysplit-dump/']
	- outfile_name: ['outfile']
    
    COMMENTS
    At this stage only one trajectory endpoint is specified, as the code 
    is currently being developed for use in back trajectory analysis. This
    will most likely be improved upon at a later date.
    """

    fid=open(infile,'w')
    
    print >>fid,date

    print >>fid,num_trajs

    for k in range(0,num_trajs):
	print "k=", k
	print "traj_endpts=","traj_endpts"
	print >>fid, '%3.4f %3.4f %3.0f' % (traj_endpt[0], traj_endpt[1], traj_endpt[2]) 
    
    print >>fid,run_time
    print >>fid,vert_mode
    print >>fid,model_top
    print >>fid,num_datasets
    print >>fid,dataset_dir
    print >>fid,dataset_name
    print >>fid,outfile_dir
    print >>fid,outfile_name

    fid.close


# def ModifyInfile(infile,)
