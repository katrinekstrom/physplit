# Introduction #

So... Maybe this page will help me get the code in order before I upload the inaugural version, which I plan to do before packing up today and going home. Ultimately this page will serve as a root to all general descriptions code.

Broadly speaking, the code can be categorised into six major sections. The following  modules are being developed to handle:

  1. **physplit.conf**: Specification of problem (model domain, data sources, pollutant characteristics etc.)
  1. **physplit.exec**: I/O to the hysplit numerical crunching machine
  1. **physplit.arch**: Output data archiving and retrieval
  1. **pyhsplit.plot**: Plotting and presentation of results
  1. **physplit.diag**: Diagnostic tools
  1. **physplit,main**: "One to rule them all and in the darkness bind them" I'm not actually THAT nerdy... I had to look that up =)

Each of these is outlined briefly here and more details will be added on separate wiki pages as I go through and work them all out.

# Details #

## physplit.conf ##

This module contains a set of tools to specify the parameters that hysplit will use in its numerical routines. These include, but are by no means limited to, the following:

  1. Input meteorological data sources
  1. Period of interest
  1. Sources locations of pollutants (or endpoints if running in reverse)
  1. Model vertical dynamics

There is heaps of documentation about the requirements of hysplit available [here](http://www.arl.noaa.gov/ready/hysp_info.html), it's not within the scope of this page to describe how hysplit works. The task of this module is to provide all of these details in the picky namelist file format required by hysplit, in such a way that the process can be automated to run many times, with variation of parameters, without user interactivity. This is of the things that makes python such a useful tool to work with.

The module also provides inverse functions to read the namelist files and return the parameters they contain. Or does it?

## physplit.exec ##
The only module that speaks directly to the hysplit program. Does some basic error checking and sanity checks before passing the information within the namelist file to hysplit for execution. Gives SENSIBLE error messages (yeah right!) upon failure to complete.

## physplit.arch ##
The model is not quick, so why run it multiple times for the same case? A set of archiving tools to search for, read and write the output files from hysplit for easy access later on. pretty boring, but useful for writing papers and going back over your results.

## physplit.plot ##
Based on pythons matplotlib, a module containing some scripts that I'm going to use to make my presentation-grade figures. Sweet eh?

