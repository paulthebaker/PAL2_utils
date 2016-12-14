#!/usr/bin/env python
"""make_hdf5.py
read in par/tim files and write to a new hdf5 file
"""

from __future__ import (division, print_function)

import glob

from PAL2 import PALdatafile

# use Steve's preprocessed parfiles!
datadir = '../iptadr2v1.051216'
pars = glob.glob(datadir + '/J*/*v1.strip.par') 
tims = glob.glob(datadir + '/J*/*v1.tim')

# sort 
pars.sort()
tims.sort()

# make hdf5 file
h5filename = 'IPTA_dr2.hdf5'
df = PALdatafile.DataFile(h5filename)

# add pulsars to file
for p, t in zip(pars, tims):
    df.addTempoPulsar(p, t, iterations=0)

