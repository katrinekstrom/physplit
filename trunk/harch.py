"""Archive and retrieval tools for hysplit output files"""
import numpy as n


def GetTrajectories(height=[500.], 
		    time_frame=[6073100,6080100],
		    archive_dir='../back-trajectories/archive/'):
    """Function to read header file of saved trajectories to catalog database
    
    USAGE: 	GetTrajectories(height,time_frame,archive_dir)
		- As many heights as you like!
		- Elements of the form YMMDDHH. Put the time_frame entries in increasing 
		  order. Please. You have three options:
		    1. One element (or integer) 
		    2. Two list elements, will return all trajectories matching your height
		       between these dates
		    3. More than three elements, will return all trajectories matching date 
		       AND height.
		
    BUGS: 	stupid python assumes any number starting with 0 is base-8, so my 
		standard naming system fails here. Works if you drop the 0.
    """
    import os

    dir_cts=os.listdir(archive_dir)
    traj_out=[]

    # force heights to list if there is only one value
    try: 
	num_heights=height.__len__()
    except AttributeError:
	num_heights=1
	height=[height]

    # force time_frame to list also
    try:
	time_frame.__len__()
    except AttributeError:
	time_frame=[time_frame]
    
    for k in range(0,dir_cts.__len__()):
	filename=dir_cts[k]
	infile=archive_dir+filename
#	print 'DEBUG:\n', dir_cts[k] 
	end_time=int(dir_cts[k].split('-')[1])

	if ( (time_frame.__len__() < 3) and ((end_time >= time_frame[0]) and (end_time <= time_frame[-1])) ) or (time_frame.__len__() >= 3 and any(n.array(time_frame) == end_time)):
	    trajectories=ReadTrajOutfile(infile)

	    for j in range(0,trajectories.__len__()):
		for k in range(0,num_heights):
#		print 'DEBUG:\n', trajectories[k]['endpoint'][2]
		    if (trajectories[j]['endpoint'][2] == height[k]):
			traj_out.append(trajectories[j])

    print ('number of trajectories in database = %d\n' % traj_out.__len__())

    return traj_out

def Date2Code(year, month, day, hour):
    return int('20'+str(year).zfill(2)+str(month).zfill(2)+str(day).zfill(2)+str(hour).zfill(2))

def AppendTrajOutfile():
    """ToDo: Wrapper for SaveTrajOutfile() to avoid unnecessary overwrites """
    return None

def SaveTrajOutfile(TrajOutfile,TrajInfile,
		    archive_dir='/media/sda4/back-trajectories-data/archive/',
		    no_save=False,
		    interactive=True):
    """Save hysplit output file to archive for later accessi
    Reads essential details from Infile used by hysplit to generate trajectory data, 
    and uses this to generate an archive name. Saves this to archive directory. For 
    now, this will overwite existing archive files with the same name, in future ver-
    sions it will append the existing file. If I feel this is necessary.
    """
    import os
    from sys import stdin
    from htools import strl2numl

    flags=[]
    fid=open(TrajInfile)
    str_cnts=fid.readline().split()


    end_time='20'
    for k in range(0,str_cnts.__len__()): 
	end_time += str_cnts[k]

    num_trajs=int(fid.readline().split()[0])
    
    # skip endpoint data
    for k in range(0,num_trajs):
	fid.readline()

    traj_age=int(fid.readline().split()[0])
    
    fid.close()

    filename= '%sbt-%s-%d.dat' % (archive_dir,end_time,-traj_age)

    if no_save: 
	flags.append('N')
	return flags,filename

    cmd = 'cp -f %s %s' % (TrajOutfile,filename)
    
    
    # Check outfile directory
    if not os.path.isdir(archive_dir):
	print 'Create directory '+archive_dir+'?', '\nProceed? [y]es/(n)o'

	answer=raw_input()

	if (answer == 'y') or (answer == ''):
	    print cmd
	    os.mkdir(archive_dir)
	else: 
	   raise OSError('No such file or directory:',archive_dir) 

    if interactive or os.path.isfile(filename):
    
	print 'I will do the following:\n', cmd, '\nProceed? [y]es/(n)o/(e)xit'
	if os.path.isfile(filename):
	    print 'WARNING: file exists!! Overwrite?'

	answer = raw_input()
	if (answer == 'y') or (answer == ''):
	    print cmd
	    os.system(cmd)
	    flags.append('0')
	elif (answer == 'n'):
	    print 'OK, maybe next time ;]' 
	    flags.append('N')
	else: 
	    print '\nAbort...'
	    flags.append('A')

    else: 
	os.system(cmd)
	flags.append('0')

    return flags,filename

def ReadConcOutfile(conc_outfile):

    fid=open(conc_outfile)

    data=fid.readlines()

    lon=n.array([0.]*(data.__len__()-1))
    lat=n.array([0.]*(data.__len__()-1))
    conc=n.array([0.]*(data.__len__()-1))

    k=-1
    for row in data:
	if k<0:
	    data_fields=row.split()
	    k+=1
	else:
	    row=row.split()
	    lat[k]=float(row[2])
	    lon[k]=float(row[3])
	    conc[k]=float(row[4])
	    k+=1
	
    lon=n.unique(lon)
    lat=n.unique(lat)
    conc_array=n.zeros((lon.__len__(),lat.__len__()))
    
    k=0
    conc_idx=0
    for lon_val in lon:
	conc_array[k,:]=conc[conc_idx:conc_idx+lat.__len__()]
	conc_idx+=lat.__len__()
	k+=1

    return lon,lat,conc_array

#def ReadConcOutfile_old(conc_outfile):
#    import csv
#
#    fid=open(conc_outfile)
#
#    data=fid.readlines()
#
#    lon=[0.]*data.__len__()
#    lat=[0.]*data.__len__()
#    conc=[0.]*data.__len__()
#
#    k=-1
#    for row in data:
#	if k<0:
#	    data_fields=row.split()
#	    k+=1
#	else:
#	    row=row.split()
#	    lat[k]=float(row[2])
#	    lon[k]=float(row[3])
#	    conc[k]=float(row[4])
#	    k+=1
#    
#
#    
#    return lon,lat,conc

def ReadTrajOutfile(trajfile='default',header_only=False):
    """ Read the data in the hysplit output trajectory file and return as a data structure"""
    from sys import stdin
    from htools import strl2numl

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
	data_list=data[k].split()
	traj_num=int(data_list[0])
	point_num=k/num_trajs

	# newitem=n.array( strl2numl(data_list[13:],'float')  )
	# print 'newitem=',newitem
	# print 'olditem=',trajectories[traj_num-1]['userdata'][point_num]

#	print data_list[0:2]
#	print data_list[2:7]
	try:
	    trajectories[traj_num-1]['timestamp'][point_num]= n.array( strl2numl(data_list[2:7])  )
	    trajectories[traj_num-1]['age'][point_num]	= n.array( strl2numl([data_list[8]],'float')  )
	    trajectories[traj_num-1]['position'][point_num] = n.array( strl2numl(data_list[9:12],'float')  )
	    trajectories[traj_num-1]['userdata'][point_num] = n.array( strl2numl(data_list[12:],'float')  )
	except IndexError:
	    pass

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

