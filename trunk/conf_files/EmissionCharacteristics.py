import numpy as n


def CreateEmissionsDictionary(num_pollutants,
				em_rate=1.,
				em_dur=1.,
				rel_date='06 07 26 00 00',
				particle=True,
				dry_dep=True,
				wet_dep=True,
				):

    """Create dictionary of emission characteristics for hymodelc input file generator 
    
    Description

    To run the dispersion component of its model, hysplit requires inputs describing emission 
    source characteristics and pollutant deposition characteristics. It also wants to have a 
    grid defined to expess its results over, otherwise it will run the model without giving 
    results. There is a little too much to include in the WriteConcInfile() function, so it is 
    bundled into dictionaries here and called from WriteConcInfile().
    
    USAGE

    
    
    """
    
    P = []
    D = []    

    for k in range(0,num_pollutants):
	a={}
	b={}
	a['Identification'] 	= 'T%d' % k
	a['EmissionRate'] 	= em_rate
	a['EmissionDuration'] 	= em_dur
	a['ReleaseDate']	= rel_date
	P.append(a)

	if particle: b['Geometry'] = n.array([5., 6., 1.])
	else: b['Geometry'] = n.array([0., 0., 0.])

	if dry_dep: b['DryPars'] = n.array([0.006, 0.0, 0.0, 0.0, 0.0])
	else: b['DryPars'] = n.array([0., 0., 0., 0., 0.])

	if wet_dep: b['WetPars'] = n.array([1.0E+05, 3.2E+05, 5.0E-05])
	else: b['WetPars'] = n.array([0., 0., 0.])

	b['Tau'] = n.array([0.])
	b['Resus'] = n.array([0.])
	D.append(b)

    return P,D


def DefineLocalGrid(num_grids,centre=n.array([-33.1858, 138.0169]),
			    spacing=[0.02,0.02],
			    span=[10., 10.],
			    vert_levels=[1],
			    level_hgts=[100],
			    sample_start=['06 07 28 00 00'],
			    sample_stop=['06 07 30 00 00'],
			    sample_int=['00 12 00']):

    G = []

    for k in range(0,num_grids):
	a={}
	a['Spacing'] = spacing[k]
	a['Span'] = span[k]
	a['NumLevels'] = vert_levels[k]
	a['LevelHgts'] = level_hgts[k]
	a['SampleStart'] = sample_start[k]
	a['SampleStop'] = sample_stop[k]
	a['SampleInt'] = sample_int[k]
	G.append(a)



