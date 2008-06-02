import pycluster.cluster
import numpy as n
import physplit
hplot=physplit.hplot; main=physplit.main
from pylab import *
from copy import deepcopy

a_small_number=1e-8

def RMSD(trajs,distance_measure):
    """Calculate root-mean-squared-deviation as per Jorba et al (1994)
    
    INPUTS:
    trajs: set of trajectories
    distance_measure(traj1,traj2): measure of difference between two trajectories
    
    """
    num_trajs=len(trajs)

    mean_trajectory=MeanTrajectory(trajs)
    deviations=[]

    for traj in trajs:
	deviations.append(distance_measure(traj,mean_trajectory))

    rmsd=sqrt(sum(array(deviations)**2)/num_trajs)
    return rmsd


def HierarchicalTrajClustering(t_in,cluster_level,distance_measure):
    """Function with plugin options to cluster trajectories"""
    global MEAN_GCD, IDX, INVERSE_COVARIANCE_MATRICES
    IDX=0

    trajs=deepcopy(t_in)
    cartesian_coords_flag=False

    if distance_measure is GreatCircleMeasure:
	MEAN_GCD=GetMeanGCD(t_in)
    elif distance_measure in [traj_euclidian_distance, MahalanobisDistance]:
	from pyproj import Proj
	lat_0=trajs[0]['position'][0,0]
	lon_0=trajs[0]['position'][0,1]
	proj=Proj(proj='lcc',lat_0=lat_0,lon_0=lon_0,lat_1=lat_0+5,lat_2=lat_0-5)
	trajs=LatLon2LCC(trajs,proj)
	cartesian_coords_flag=True

    if distance_measure is MahalanobisDistance:
	mean_traj,cov_mats=GetTrajStats(trajs)
	INVERSE_COVARIANCE_MATRICES=[]
	print "Determining covariance matrices for trajectory endpoints..."
	for  mat in cov_mats:
	    try: 
		INVERSE_COVARIANCE_MATRICES.append(n.linalg.inv(mat))
	    except n.linalg.LinAlgError: 
		INVERSE_COVARIANCE_MATRICES.append(n.matrix(n.eye(3)))
	print "Done."

    if hasattr(trajs[0]['age'],'tolist'):
	print "converting arrays to lists..."
	convert_arrays_to_lists(trajs)
	print "Done."

    print "Finding clusters..."
    cl=pycluster.cluster.HierarchicalClustering(trajs,distance_measure)
    traj_clusters=cl.getlevel(cluster_level)
    print "Done."

    print "HierarchicalTrajClustering:", len(traj_clusters), " clusters identified"
    
    idx=0
    rmsd_list=[]
    for cluster in traj_clusters:
	convert_lists_to_arrays(cluster)
	if cartesian_coords_flag:
	    traj_clusters[idx]=(LatLon2LCC(cluster,proj,inv=True))
	rmsd_list.append(RMSD(cluster,distance_measure))
	print "Cluster", str(idx+1).zfill(2)+":", len(cluster), "trajectories, ", rmsd_list[idx], "RMS variance" 
	idx+=1

    # print "measure function called", IDX, "times."

    return traj_clusters, rmsd_list

def PlotTrajClusters(traj_clusters):
    """Script to plot trajectory clusters"""
    ioff()

    num_clusters=len(traj_clusters)
    clrs=hplot.ColorSpectrum(num_clusters,return_as_tuples=True)
    map=physplit.main.PlotTraj([],plot_tracks=False,return_map=True)

    figure(1)
    idx=0
    for cluster in traj_clusters:
	# for traj in cluster:
	hplot.PlotTrajectories(cluster,map,time_increments=[],plot_legend=False,\
		clrs=clrs[idx],alpha=0.7)
	idx+=1
    
    figure(2)
    idx=0
    for cluster in traj_clusters:
	# for traj in cluster:
	hplot.VerticalProfiles(cluster,time_increments=[],plot_legend=False,\
		clrs=clrs[idx],alpha=0.7)
	idx+=1

    figure(1)
    map.drawmapboundary()
    map.drawcoastlines()
    map.drawmeridians(arange(90,161,5),labels=[1,0,0,1])
    map.drawparallels(arange(-60,0,5),labels=[1,0,0,0])
    title('Trajectory Track Envelopes')

    figure(2)

    show()

    return

def MahalanobisDistance(t1,t2):
    """Multivariate scale independent measure for comparison between two trajectories
    
    Imlements comparison of height between two trajectories
    """
    global INVERSE_COVARIANCE_MATRICES

    try: INVERSE_COVARIANCE_MATRICES
    except NameError:
	print "Covariance matrices not specified. Using euclidian_distance(t1,t2)" 
	distance=traj_euclidian_distance(t1,t2)
	return distance

    num_pts=len(t1['age'])

    mahal_dist=[]

    for idx in range(0,num_pts):
	diff_vec=(n.matrix(t1['position'][idx])-n.matrix(t2['position'][idx])).T
	inv_cov_mat=INVERSE_COVARIANCE_MATRICES[idx]
	# if idx == 4:
	    # raise n.linalg.LinAlgError, "singular Matrix"
	dist=sqrt( diff_vec.T*inv_cov_mat*diff_vec )
	mahal_dist.append(dist[0,0])
    return sum(mahal_dist)

def GreatCircleMeasure(t1,t2):
    """Defines a basis for comparison between two trajectories
    
    This function returns a measure of the similarity between two trajectories based on 
    the great circle distance between trajectory endpoints.

    TODO:
    - reduce number of points used... maybe to 3- or 6-hourly
    - introduce Mahalanobis distance instead of normalising wrt averages
    - implement measure of height in addition to global position


    """
    from pyproj import Geod
    global MEAN_GCD

    traj1=deepcopy(t1); traj2=deepcopy(t2)

    if hasattr(traj1['age'],'tolist'):
	convert_arrays_to_lists([traj1])
    if hasattr(traj2['age'],'tolist'):
	convert_arrays_to_lists([traj2])

    geo=Geod(ellps='clrk66')
    num_pts=len(traj1['age'])
    lats0=[traj1['position'][0][0]]*num_pts
    lons0=[traj1['position'][0][1]]*num_pts

    lats1=[]; lons1=[]; lats2=[]; lons2=[]
    idx=0

    for endpoint in traj1['position']:
	lats1.append(traj1['position'][idx][0])
	lats2.append(traj2['position'][idx][0])
	lons1.append(traj1['position'][idx][1])
	lons2.append(traj2['position'][idx][1])
	idx+=1

    gcd_1_2=geo.inv(lons1,lats1,lons2,lats2)[2]

    try: mean_gcd=MEAN_GCD
    except NameError:
	print "GreatCircleMeasure: using local MEAN_GCD"
	mean_gcd=GetMeanGCD([t1,t2])
    
    gcd_norm=array(gcd_1_2)/(array(mean_gcd)+a_small_number)
    # gcd_measure=sum(gcd_1_2)
    return sum(gcd_norm)

def GetTrajStats(trajectories):
    """Basic statistical analysis of three dimensional data.

    Determines trajectoy position means and covariances for hourly positions.
    
    INPUTS
	trajectories - same old structure, or any list of dictionaries containing
			at least "position" 
    OUTPUTS
	traj_mean - mean positions... most meaningful if cartesian positions are 
			used instead of geographical (lat lon)
	covariance_matrices - 3x3xK array, where K is the number of data points 
			in the trajectory. The user should check the consisteny
			of this value, as there is no way the clustering will be
			if this is not satisfied!!
    """
    from copy import deepcopy

    num_trajs=len(trajectories)
    num_pts=len(trajectories[0]['age'])

    # preallocate
    coord_data=n.zeros([num_pts,num_trajs,3])

    # extract data from trajctory structures
    idx=0
    for traj in trajectories:
	coord_data[:,idx,0]=traj['position'][:num_pts,0]
	coord_data[:,idx,1]=traj['position'][:num_pts,1]
	coord_data[:,idx,2]=traj['position'][:num_pts,2]
	idx+=1

    # evaluate covariance matrices and means
    covariance_matrices=[]
    traj_mean=n.zeros([num_pts,3])
    for idx in range(num_pts):
	covariance_matrices.append(n.matrix(n.cov(coord_data [idx,:,:],rowvar=0)))
	traj_mean[idx,:]=mean(coord_data[idx,:,:],axis=0)

    return traj_mean,covariance_matrices

def LatLon2LCC(trajs, proj, inv=False):
    """Convert ground trajectories between Cartesian and Geographocal coordinates.

	INPUTS:
	trajs - list of trajectory data structures. At a minimum, a list of 
		dicts containing a "position" field which is an array, the 
		first 2 columns of which are "lat" and "lon" data points, in
		degrees, respectively.
	proj  - pyproj.Proj() object defining the projection used in the mapping.
	inv   - [False] By default do the forward transformation
    """
    from copy import deepcopy
    trajs_out=[]
    for traj in trajs:
	# preserve input
	traj_new=deepcopy(traj)
	# lats OR x 
	coords_in_0=list(traj['position'][:,0])
	# lons OR y 
        coords_in_1=list(traj['position'][:,1])
	
	# A little manipulation is required since the trajectory structs have lat/lon
	# in funny places
	if inv:
	    # inverse transform is x,y->lons,lats
	    coords_out_0,coords_out_1=proj(coords_in_0,coords_in_1,inverse=True)
	    # lats
	    traj_new['position'][:,0]=coords_out_1
	    # lons
	    traj_new['position'][:,1]=coords_out_0
	else:
	    # forward transform is lons,lats->x,y
	    coords_out_0,coords_out_1=proj(coords_in_1,coords_in_0)
	    # x
	    traj_new['position'][:,0]=coords_out_0
	    # y
	    traj_new['position'][:,1]=coords_out_1
	
	trajs_out.append(traj_new)
    
    return trajs_out

def convert_arrays_to_lists(list_of_dicts):
    """pycluster is REALLY fussy about the format of the data structures. This fucntion converts
    the fields of the trajectory data structure into lists"""

    for dict in list_of_dicts:
	for key in dict.keys():
	    if key in ['position','age','userdata']:
		dict[key]=dict[key].tolist()

def convert_lists_to_arrays(list_of_dicts):
    """Converts the trajectory data structure back to how it should be"""

    for dict in list_of_dicts:
	for key in dict.keys():
	    if key in ['position','age','userdata']:
		dict[key]=n.array(dict[key])


def euclidian_distance(traj1,traj2):
    distance=sum(sqrt (sum(  (traj2['position']-traj1['position'])**2,axis=0)  ) )
    return distance

def traj_euclidian_distance(t1,t2):
    global IDX
    try: IDX+=1
    except NameError: pass
    distance=sum( sqrt( sum( (array(t2['position'])-array(t1['position']))**2,axis=1 ) ) )
    return distance

def MeanTrajectory(trajectories):
    from copy import deepcopy

    num_trajs=len(trajectories)
    num_pts=len(trajectories[0]['age'])

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

def GetMeanGCD(trajs):
    """Normalising factor for cluster algorithm"""
    from pyproj import Geod

    num_pts=len(trajs[0]['age'])
    geo=Geod(ellps='clrk66')

    lats0=[trajs[0]['position'][0][0]]*num_pts
    lons0=[trajs[0]['position'][0][1]]*num_pts


    num_trajs=len(trajs)

    gcd=n.zeros([num_pts,num_trajs])

    idx=-1
    for traj in trajs:
	idx+=1
	lats1=list(traj['position'][:num_pts][:,0])
	lons1=list(traj['position'][:num_pts][:,1])
	gcd[:,idx]=geo.inv(lons0,lats0,lons1,lats1)[2]

    return list(mean(gcd,axis=1))

def Trajs2CartTuple(trajs,num_pts=36):

    lat_parameter=cos(36.3869*n.pi/180)
    degrees2metres=111170

    lat0=array([-36.3869]*num_pts)
    lon0=array([148.394]*num_pts)

    out_list=[]

    for traj in trajs:
	new_list=[]
	delta_x=(traj['position'][:num_pts][:,0]-lat0)*degrees2metres*lat_parameter
	delta_y=(traj['position'][:num_pts][:,1]-lon0)*degrees2metres
	for idx in range(len(delta_x)):
	    new_list.append((delta_x[idx],delta_y[idx]))
	out_list.append(tuple(new_list))

    return out_list

## BROKEN CODE ##
# def KMeansTrajClustering(t_in,num_clusters):
#     """Function with plugin options to cluster trajectories"""
#     global MEAN_GCD
# 
#     # trajs_cartesian=LatLon2Cartesian(trajs)
#     trajs=deepcopy(t_in)
# 
#     if hasattr(trajs[0]['age'],'tolist'):
# 	convert_arrays_to_lists(trajs)
#     cl=pycluster.cluster.KMeansClustering(trajs,GreatCircleMeasure)
#     traj_clusters=cl.getclusters(num_clusters)
# 
#     for cluster in traj_clusters:
# 	convert_lists_to_arrays(cluster)
# 
#     return traj_clusters

# def Cartesian2LatLon(trajs_cart,projection='clrk66'):
# 
#     from pyproj import Geod
#     from copy import deepcopy
# 
#     trajs_cart=[]
# 
#     for traj in trajs_cart:
# 	traj_new=deepcopy(traj)
#         num_pts=len(traj['position'][:,0])
#         geo=Geod(ellps=projection)
# 
# 	# initial and terminus points
# 	x_0=[traj['position'][0,0]]*num_pts
# 	y_0=[traj['position'][0,1]]*num_pts
#         x_a=list(traj['position'][:,0])
#         y_a=list(traj['position'][:,1])
#     return None

# def LatLon2Cartesian(trajs):
#     """Return trajectory in terms of cartesian coordinates wrt arrival location """
# 
#     from pyproj import Geod
#     from copy import deepcopy
# 
#     trajs_cart=[]
# 
#     for traj in trajs:
# 
#         traj_new=deepcopy(traj)
#     
#         num_pts=len(traj['position'][:,0])
#         
#         geo=Geod(ellps='clrk66')
#         lats0=[traj['position'][0][0]]*num_pts
#         lons0=[traj['position'][0][1]]*num_pts
#     
#         lats1=list(traj['position'][:,0])
#         lons1=list(traj['position'][:,1])
#      
#         x_info=geo.inv(lons0,lats0,lons1,lats0)
#         # Use the back azimuth to define the sign of x
#         x=x_info[2]*n.sign(x_info[0])
#     
#         y_info=geo.inv(lons0,lats1,lons0,lats0)
#         y=y_info[2]*n.sign( -(n.abs(y_info[1])-90) )
#     
#         traj_new['position'][:,0]=x
#         traj_new['position'][:,1]=y
#         # traj_new['position']=traj_new['position'].tolist()
# 
# 	trajs_cart.append(traj_new)
#     
#     return trajs_cart
