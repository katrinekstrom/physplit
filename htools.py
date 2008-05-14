#!/usr/bin/python
"""General tools that i will be calling from wherever i feel like forever amen"""

import numpy as n

def Traj_Cyl_Coords(traj, inv=True):
    """Convert points on a trajectory into cylindrical coordinates WRT endpoint.
    
    To convert back to cartesian, set inv=False
    """

    from copy import deepcopy
    from pyproj import Geod

    geo=Geod(ellps='clrk66')
    traj_new_coords=deepcopy(traj)
    num_pts=len(traj['age'])

    traj_coord0=traj['position'][:,0] #cart->lats,cyl->r
    traj_coord1=traj['position'][:,1] #cart->lons,cyl->theta

    end_lats=n.array([traj['endpoint'][0]]*num_pts)
    end_lons=n.array([traj['endpoint'][1]]*num_pts)

    if inv:
	# print len(end_lons),len(end_lats),len(traj_coord1),len(traj_coord0)
        new_coords=geo.inv(end_lons.tolist(),end_lats.tolist(),traj_coord1.tolist(),traj_coord0.tolist())
	traj_new_coords['position'][:,0]=new_coords[2]
	traj_new_coords['position'][:,1]=new_coords[0]
    else:
        new_coords=geo.fwd(end_lons,end_lats,traj_coord1,traj_coord0)
	traj_new_coords['position'][:,0]=new_coords[1]
	traj_new_coords['position'][:,1]=new_coords[0]

    return traj_new_coords

def MeanTrajectory(trajectories,num_pts=48):
    from copy import deepcopy

    num_trajs=len(trajectories)
    # num_pts=len(trajectories[0]['age'])

    # preallocate
    lats=n.zeros([num_pts,num_trajs])
    lons=n.zeros([num_pts,num_trajs])
    hts=n.zeros([num_pts,num_trajs])

    idx=0
    for traj in trajectories:
	lats[:,idx]=traj['position'][:num_pts,0]
	lons[:,idx]=traj['position'][:num_pts,1]
	hts[:,idx]=traj['position'][:num_pts,2]
	idx+=1

    mean_lat=n.mean(lats,axis=1)
    mean_lon=n.mean(lons,axis=1)
    mean_ht=n.mean(hts,axis=1)
    
    mean_traj={}
    mean_traj['position']=n.zeros([num_pts,3])
    
    mean_traj['position'][:,0]=mean_lat
    mean_traj['position'][:,1]=mean_lon
    mean_traj['position'][:,2]=mean_ht
    mean_traj['endtime']=[0,0,0,0]
    mean_traj['endpoint']=trajectories[0]['endpoint']
    mean_traj['age']=trajectories[0]['age'][:num_pts]

    return mean_traj

def TrajectoryEnvelope(trajectories,num_pts=48):
    from copy import deepcopy

    num_trajs=len(trajectories) 
    
    rng=n.zeros([num_pts,num_trajs])
    azi=n.zeros([num_pts,num_trajs])
    hgt=n.zeros([num_pts,num_trajs])

    mean_traj=MeanTrajectory(trajectories,num_pts)
    mean_traj=Traj_Cyl_Coords(mean_traj)

    idx=0
    for traj in trajectories:
	# print idx
	traj_cyl=Traj_Cyl_Coords(traj)
	rng[:,idx]=traj_cyl['position'][:num_pts,0]
	azi[:,idx]=traj_cyl['position'][:num_pts,1]
	hgt[:,idx]=traj_cyl['position'][:num_pts,2]
	idx+=1

#    mean_rng=n.mean(rng,axis=1)
#    mean_azi=n.mean(azi,axis=1)
#    mean_hgt=n.mean(hgt,axis=1)
    
    std_rng=n.std(rng,axis=1)
    std_azi=n.std(azi,axis=1)
    std_hgt=n.std(hgt,axis=1)

#    mean_traj={}
#    mean_traj['position']=n.zeros([num_pts,3])
#    
#    mean_traj['position'][:,0]=mean_rng
#    mean_traj['position'][:,1]=mean_azi
#    mean_traj['position'][:,2]=mean_hgt
#    mean_traj['endtime']=[0,0,0,0]
#    mean_traj['endpoint']=trajectories[0]['endpoint']
#    mean_traj['age']=trajectories[0]['age'][:num_pts]

    outer_traj_1=deepcopy(mean_traj)
    outer_traj_2=deepcopy(mean_traj)

    outer_traj_1['position'][:,1]+=std_azi
    outer_traj_1['position'][:,2]+=std_hgt

    outer_traj_2['position'][:,1]-=std_azi
    outer_traj_2['position'][:,2]-=std_hgt

    mean_traj=Traj_Cyl_Coords(mean_traj,inv=False)
    outer_traj_1=Traj_Cyl_Coords(outer_traj_1,inv=False)
    outer_traj_2=Traj_Cyl_Coords(outer_traj_2,inv=False)

    return [mean_traj],[outer_traj_1,outer_traj_2]

#def TrajectoryStats(trajectories):
#    from copy import deepcopy
#
#    num_trajs=len(trajectories)
#    num_pts=48
#    # num_pts=len(trajectories[0]['age'])
#
#    # preallocate
#    lats=n.zeros([num_pts,num_trajs])
#    lons=n.zeros([num_pts,num_trajs])
#    hts=n.zeros([num_pts,num_trajs])
#
#    idx=0
#    for traj in trajectories:
#	lats[:,idx]=traj['position'][:num_pts,0]
#	lons[:,idx]=traj['position'][:num_pts,1]
#	hts[:,idx]=traj['position'][:num_pts,2]
#	idx+=1
#
#    mean_lat=n.mean(lats,axis=1)
#    mean_lon=n.mean(lons,axis=1)
#    mean_ht=n.mean(hts,axis=1)
#    
#    std_lat=n.std(lats,axis=1)
#    std_lon=n.std(lons,axis=1)
#    std_ht=n.std(hts,axis=1)
#
#    mean_traj={}
#    mean_traj['position']=n.zeros([num_pts,3])
#    
#    mean_traj['position'][:,0]=mean_lat
#    mean_traj['position'][:,1]=mean_lon
#    mean_traj['position'][:,2]=mean_ht
#    mean_traj['endtime']=[0,0,0,0]
#    mean_traj['endpoint']=trajectories[0]['endpoint']
#    mean_traj['age']=trajectories[0]['age'][:num_pts]
#
#    outer_traj_1=deepcopy(mean_traj)
#    outer_traj_2=deepcopy(mean_traj)
#
#    outer_traj_1['position'][:,0]+=std_lat
#    outer_traj_1['position'][:,1]-=std_lon
#    outer_traj_1['position'][:,2]+=std_ht
#
#    outer_traj_2['position'][:,0]-=std_lat
#    outer_traj_2['position'][:,1]+=std_lon
#    outer_traj_2['position'][:,2]-=std_ht


    return [mean_traj,outer_traj_1,outer_traj_2]

def SortTrajectories(trajectories,by_var='end_height'):
    """sort trajectory data structure as defined by ReadTragfile by one of its variables

    USAGE:
    by_var can be 'height' or 'enddate'... so far...
    """
    # import ArchiveControl as AC
    import physplit.harch as harch

    num_trajs=trajectories.__len__()
    the_index=n.zeros([1,num_trajs])

    for k in range(0,num_trajs):
	if (by_var == 'end_height'):
	    the_index[0,k] = (trajectories[k]['position'][0,2])
	elif (by_var == 'end_date'):
	    et = trajectories[k]['endtime']
	    the_index[0,k] = harch.Date2Code(et[0],et[1],et[2],et[3]) 

    inx = permutation_indices(the_index)

    # end_height=end_height[0][inx]
    dummy=[]

    for k in inx:
	dummy.append(trajectories[k].copy())

    trajectories=dummy

    return trajectories

def permutation_indices(data,reverse=False):
    """function to return the indeces of a sort mapping, modified to handle arrays"""
    
    # check to see if 'data' is array type
    if hasattr(data,'shape'):
	data = data.tolist()

    shp = n.shape(data)
    dims = len(shp)

    if dims>1:
	if shp[0]>1:
	    return n.NaN
	elif shp[0]==1:
	    data = data[0]

    return sorted(range(len(data)), key = data.__getitem__, reverse=reverse)
    


def strl2numl(lst,format='int'):

    numels=len(lst)
    lst_out=[]

    for k in range(0,numels):
	if format == 'int':
	    lst_out.append(int(lst[k]))
	elif format == 'float':
	    lst_out.append(float(lst[k]))

    return lst_out

def unique2d(arr,axis=0):
    """function to sort and eliminate replicate rows/columns of an array. Extension to numpy's unique()
   
   USAGE:
   arr  : 2d array at this stage
   axis : sort by axis = [0],1 ([rows],cols)
    """

    I=[]

    # check shape of arr
    rows,cols=arr.shape
    
    # to sort by cols, transpose and do the same as you would for rows
    if axis==1:
	arr=arr.T

    for k in range(0,cols):
	i,d=n.unique1d(arr[:,k],return_index=True)
	I=n.hstack((I,i))
    I=n.unique1d(I)
    I=I.tolist()
    arr_out = arr[I,:]

    if axis==1:
	arr_out=arr_out.T

    return arr_out
    
