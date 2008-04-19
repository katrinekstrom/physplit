#!/usr/bin/python
"""Suite to configure hysplit inputs

This module is a set of functions to control all of the read/write to 
the namelist files for hysplit.

Copyright (C) Thomas Chubb 2008
"""

import numpy as n
import mydatetime.mydatetime as cal
import datetime as dt

def select_GDAS_files(date_list,dataset_file_list):

    filenames=[]

    for date in date_list:
	yr,mn,dy,hr=cal.decompose_date(date)
	# get the week this day falls in, and the week before
	weeks=[dy/7,dy/7+1]
	for wk in weeks: 
	    if wk==0:
		dataset_filenames=['gdas1.'+cal.month_names[mn-2]+str(yr)[-2:]+'.w5',\
			'gdas1.'+cal.month_names[mn-2]+str(yr)[-2:]+'.w4']
	    else:
		dataset_filenames=['gdas1.'+cal.month_names[mn-1]+str(yr)[-2:]+'.w'+str(wk)]

	    for dataset in dataset_filenames:
		if dataset in dataset_file_list:
		    if dataset not in filenames:
			filenames.append(dataset)

		else:
		    raise NameError('required dataset not included in dataset_files:'+dataset)

    return filenames

def GenDatelist(start_date,end_date,hour_inc):

    try:
	st_yr,st_mth,st_day,st_hrs=cal.decompose_date(start_date)
	end_yr,end_mth,end_day,end_hrs=cal.decompose_date(end_date)
    except ValueError:
	print ">>> Need to include hours in date string (YYYYMMDDhh)"
	raise ValueError(">>> need more than 3 values to unpack")

    start_datetime=dt.datetime(st_yr,st_mth,st_day,st_hrs)
    end_datetime=dt.datetime(end_yr,end_mth,end_day,end_hrs)

    time_delta=dt.timedelta(0,hour_inc*3600)

    cur_datetime=start_datetime

    date_list=[]

    while cur_datetime < end_datetime:
	date_list.append(int(str(cur_datetime.year) + str(cur_datetime.month)\
		.zfill(2) + str(cur_datetime.day).zfill(2) + str(cur_datetime\
		.hour).zfill(2)))
	cur_datetime+=time_delta

    return date_list

def GenEndpts():
    """a set of endpoints, feel free to edit"""
    
    heights=n.array([])
    heights=n.append(heights,n.arange(1000,4001,1000))
    heights=n.append(heights,n.array([500]))
    #heights=n.append(heights,n.arange(200,1000,200))
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

def WriteConcInfile(infile,pollutant_data=None,grid_data=None,deposition_data=None,
			date=2006072700,
			conc_sourcepts=[-33.1858, 138.0169, 50.0],
			run_time=48,
			vert_mode=0,
			model_top=10000,
			# num_datasets=1,
			dataset_dir=['/media/sda4/hysplit-data/'],
			dataset_name=['gdas1.jul06.w4'],
			outfile_dir=['/media/sda4/hysplit-dump/']):

    """function to open and edit hymodelc input file"""
    import datetime as dt
     
    # determine total number of sources to be requested
    num_sources=len(conc_sourcepts)

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

    cur_yr,cur_mth,cur_day,cur_hr=cal.decompose_date(date)
    cur_dt=dt.datetime(cur_yr,cur_mth,cur_day,cur_hr)

    date_str=str(cur_dt.year)[-2:]+' '+str(cur_dt.month).zfill(2)+' '\
	    +str(cur_dt.day).zfill(2)+' '+str(cur_dt.hour).zfill(2)

    # date_str=cal.FormatDate(date)[0]

    # open file for write access
    fid=open(infile,'w')
    print >>fid,date_str
    print >>fid,num_sources

    for source in conc_sourcepts:
	print >>fid, '%3.4f %3.4f %3.1f' % (source[0], source[1], source[2]) 
    
    print >>fid,run_time
    print >>fid,vert_mode
    print >>fid,'%3.1f' % (model_top)
    print >>fid,num_datasets

    for k in range(0,num_datasets):
	if (num_dataset_dirs==1):
	    print >>fid,dataset_dir
	else:
	    print >>fid,dataset_dir[k]
	
	print >>fid,dataset_name[k]

    # plume release details, edit here:
    if pollutant_data is not None:
	num_pollutants=len(pollutant_data['plume_id'])
    else: 
	num_pollutants=1
	pollutant_data={}
        pollutant_data['plume_id']=['PLU1']
        pollutant_data['emission_rate']=[1000000.]
        pollutant_data['emission_time']=[96]
        pollutant_data['release_start']=[date_str]

    print >>fid, num_pollutants
    for k in range(num_pollutants):
        print >>fid, pollutant_data['plume_id'][k]
        print >>fid, pollutant_data['emission_rate'][k]
        print >>fid, pollutant_data['emission_time'][k]
        print >>fid, pollutant_data['release_start'][k]

    
    # concentration grid
    if grid_data is not None:
	num_grids=len(grid_data['lat_lon'])
    else:
	num_grids=1
	grid_data={}
	grid_data['lat_lon']=[[0.,0.]]
	grid_data['spacing']=[[.25,.25]]
	grid_data['span']=[[30.,30.]]
	grid_data['output_directory']=[['/home/tchubb/pylib/physplit/working/']]
	grid_data['output_file']=[['cdump1']]
	grid_data['num_vert_levels']=[[5]]
	grid_data['vert_levels']=[[100.,200.,500.,1000.,2000.]]
	grid_data['sampling_start']=[[date_str + ' 00']]
	stop_dt=cur_dt+dt.timedelta(4)
	stop_str=str(stop_dt.year)[-2:]+' '+str(stop_dt.month).zfill(2)+' '\
	    +str(stop_dt.day).zfill(2)+' '+str(stop_dt.hour).zfill(2)
	grid_data['sampling_stop']=[[stop_str+ ' 00']]
	# grid_data['sampling_stop']=[cal.FormatDate(cal.jump_to_date(date,2))]
	grid_data['av_now_max']=[['00','03','00']]

    print >>fid, num_grids
    for k in range(num_grids):
	for member in ['lat_lon','spacing','span','output_directory',\
		'output_file','num_vert_levels','vert_levels','sampling_start',\
		'sampling_stop','av_now_max']:
	    next_line=''
	    for thingy in grid_data[member][k]:
		next_line+= str(thingy) + ' ' 
	    print >>fid, next_line

    # deposition
    if deposition_data is not None:
	num_depositions=len(deposition_data['resuspension_factor'])
    else:
	num_depositions=1
	deposition_data={}
	deposition_data['physical_props']=[[1., 1., 1.]]
	deposition_data['dispersion_props']=[[0.006, 0., 0., 0. ]]
	deposition_data['deposition_props']=[[1., 3.2E+05, 5.0E-05]]
	deposition_data['radioactive_half_life']=[[0.]]
	deposition_data['resuspension_factor']=[[0.]]

    print >>fid, num_depositions
    for k in range(num_depositions):
	for member in ['physical_props','dispersion_props','deposition_props',\
		'radioactive_half_life','resuspension_factor']:
	    next_line=''
	    for thingy in deposition_data[member][k]:
		next_line+= str(thingy) + ' ' 
	    print >>fid, next_line

    fid.close()
    return 0

