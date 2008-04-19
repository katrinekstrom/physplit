#!/usr/bin/python
"""General tools that i will be calling from wherever i feel like forever amen"""

import numpy as n

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
    
