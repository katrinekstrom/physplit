# Introduction #

## 'physplit': 'python' + 'hysplit' ##

Yay for hysplit and yay for python. Together they will make a powerful tool for air quality modelling and pollutant dispersion simulation, as well as providing valuable insight into air parcel histories for meteorological research. The physplit project has been created to make use of some python modules developed during a research project (ongoing) by Thomas Chubb to investigate the sources of aerosols during winter storms in South-Eastern Australia and includes a pythonic command-line interface that is more powerful than the GUI distributed with Hysplit and easier to use than directly editing the Fortran namelist files used by the numerical kernel of the hysplit model. Plotting utilities based on the python matplotlib modules are included and analysis tools will be added as they are developed. if you'd like to get on board with the development or would like to try it out for yourself, give me a yell!

## NOAA Hysplit ##

The HYSPLIT (HYbrid Single-Particle Lagrangian Integrated Trajectory) model is the newest version of a complete system for computing simple air parcel trajectories to complex dispersion and deposition simulations. More info on: http://www.arl.noaa.gov/ready/hysp_info.html

## Python ##

Python is the greatest most usefullest programming language that I have used. Combined with the numeric and scientific modules (numpy and scipy), along with good plotting tool kits (matplotlib, pylab) it makes a great scientific tool as well. There are a few more things you'll need in your python miscellany, including tools to handle the formidable NetCDF file format (PyNGL, PyNIO), available from the Earth System Grid pages, but not till I get around to implementing the WRF-ARW stuff. I think I use pyproj as well, but run it and see about your errors first

## pywrf ##

You guessed it, **'pywrf' = 'python' + 'wrf'**. Here is where I plug another ongoing project, being principally maintained by the talented and wonderful Valerio Bisignesi, until he cuts and runs very shortly. Check it out [here](http://code.google.com/p/pywrf/)