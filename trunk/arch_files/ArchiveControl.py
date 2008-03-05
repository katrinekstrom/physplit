#!/usr/bin/python
"""Small suite to control saving to and retrieval from back trajectory archive

Copyright (C) Thomas Chubb 2007
"""
import numpy as n

# TODO: Replace the calendar stuff with the much better suite in MyDateTime. This one is crappy.
def DateItr(t1,t2,intvl):
    """Iterate on  date codes"""

    year  = int(n.floor(t1/1e6))
    m = int(n.floor(t1/1e4)-n.floor(t1/1e6)*100)
    d = int(n.floor(t1/1e2)-n.floor(t1/1e4)*100)
    h = int(t1-n.floor(t1/1e2)*100)

#    print "initial date:", year, m,d,h

    # Account for leap year
    if ((year%4)==0) and (year!=2000):
	feb=1
    else:
	feb=0

    dpm = [31,28+feb,31,30,31,30,31,31,30,31,30,31]

    code_itr = [t1]

    while 1:
	d_jump = (h+intvl)/24
	m_jump = (d+d_jump)/(dpm[m]+1)

	h = (h+intvl)%24
	if (m_jump > 0):
	    d = (d+d_jump)%dpm[m] 
	else:
	    d = d+d_jump
	m = (m+m_jump)%12
	c_next = Date2Code(year,m,d,h)

	if c_next >= t2:
	    break
	elif code_itr.__len__() > 30:
	    print "Threshold reached... exiting"
	    return 1
	else:
	    code_itr.append(c_next)

    return code_itr

def Date2Code(year,month,day,hour):
    
    # Account for leap year
    if ((year%4)==0) and (year!=2000):
	feb=1
    else:
	feb=0
    dpm = [31,28+feb,31,30,31,30,31,31,30,31,30,31]

    if year >= 1990:
	year_str=str(year)[2:]
    else: 
	year_str=str(year)
    
    # check for illegal codes...
    if (month > 12) or (month == 0):
	print "Illegal month"
	return 1
    elif month < 10:
	month_str = '0'+str(month)
    else:
	month_str = str(month)

    if day > dpm[month] or day == 0:
	print "Illegal day"
	return 1
    elif day < 10:
	day_str = '0'+str(day)
    else:
	day_str = str(day)

    if hour > 24:
	print "Illegal hour"
	return 1
    elif hour < 10:
	hour_str = '0'+str(hour) 
    else:
	hour_str= str(hour)

    out=int(year_str+month_str+day_str+hour_str)

    return out


 
def Date2Hour(t_in):
    """Converts date code to hours since 1990"""

    year  = int(n.floor(t_in/1e6))
    month = int(n.floor(t_in/1e4)-n.floor(t_in/1e6)*100)
    day   = int(n.floor(t_in/1e2)-n.floor(t_in/1e4)*100)
    hour  = int(t_in-n.floor(t_in/1e2)*100)

    if year < 10:
	year+=2000
    else:
	year+=1900 

    print year, month, day, hour

    if year<1990:
	print "choose a year later than 1990" 
	return 0

    h=0
    
    # sum hours from previous years to 1990 (arbitrary)
    for j in range(1989,year-1):

	if ((j%4)==0) and (j!=2000):
	    feb=1
	else:
	    feb=0

	h+=(365+feb)*24

    # hours in this year to date
    if ((year%4)==0) and (year!=2000):
	feb=1
    else:
	feb=0

    dpm = [31,28+feb,31,30,31,30,31,31,30,31,30,31]

    for k in range(0,month-1):
	h += dpm[k]*24

    h += (day-1)*24
    h += hour

    return h

def Hour2Date():
    """Inverse function fot Date2Hour()"""


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
    import hysplitIO as H

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
	    trajectories=H.ReadTrajOutfile(infile)

	    for j in range(0,trajectories.__len__()):
		for k in range(0,num_heights):
#		print 'DEBUG:\n', trajectories[k]['endpoint'][2]
		    if (trajectories[j]['endpoint'][2] == height[k]):
			traj_out.append(trajectories[j])

    print ('number of trajectories in database = %d\n' % traj_out.__len__())

    return traj_out

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
    from ArrayToolbox import strl2numl

    flags=[]
    fid=open(TrajInfile)
    str_cnts=fid.readline().split()

    end_time=''
    for k in range(0,str_cnts.__len__()): end_time += str_cnts[k]

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
    
    if interactive:

	print 'I will do the following:\n', cmd, '\nProceed? [y]es/(n)o/(e)xit'
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

