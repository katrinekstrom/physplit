"""Files to execute various hysplit modules and handle I/O

Copyright (C) Thomas Chubb 2008
"""

import numpy as n

def ExecHymodelt(infile='../test-data/TEST_INFILE',
		    hysplit_path='/home/tchubb/hysplit4/exec/hymodelt'):

    """define a shell command and execute to operate hysplit trajectory model"""
    import os
    import sys

    command = 'cat %s | wine %s' % (infile,hysplit_path)
    print command
    
    # Check infile location and try alternative defaults
    print 'hexec: Checking for infile %s...' % (infile)
    try:
	os.stat(infile)
    except OSError:
	print 'hexec: Unable to locate infile... exiting'
	return 1

    # Check hysplit path and try alternative defaults
    print 'hexec: Checking hysplit path %s...' % (hysplit_path)
    # this_dir=os.getcwd()
    # os.chdir(hysplit_path.rstrip('/hymodelt'))
    try:
	# os.stat('/hymodelt')
	os.stat(hysplit_path)
    except OSError:
	print 'hexec: Unable to locate hysplit... exiting'
	return 1
    # os.chdir(this_dir)

    os.system(command)
    
    return None



def ExecHymodelt_old(infile='../test-data/TEST_INFILE',
		    hysplit_path='/home/tchubb/hysplit4/exec/hymodelt'):

    """define a shell command and execute to operate hysplit trajectory model"""
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

