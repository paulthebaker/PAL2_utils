#!/usr/bin/env python
from __future__ import division

import glob, os, shutil
import argparse
import numpy as np

from matplotlib import use
use('PDF') # use non-interactive backend for cluster
import matplotlib.pyplot as plt

from PAL2 import bayesutils as bu

#####
##  ARGUMENT PARSER
#####
parser = argparse.ArgumentParser(description='run PAL2 noise analysis on IPTA pulsars')
parser.add_argument('--pulsar', action='store', required=True,
                    help='pulsar to process')
parser.add_argument('--Nburn', action='store', required=False, default=None, type=int,
                    help='number of samples to discard as burn in this is prioritized over burn-fraction')
parser.add_argument('--burn-fraction', action='store', dest='burnfrac', required=False, default=0.25, type=float,
                    help='fraction of samples to discard as burn in')

args = parser.parse_args()

this_PSR = args.pulsar

# generate directories for this_PSR
plotsdir = this_PSR+'/plots'
chaindir = this_PSR+'/chain'
if not os.path.exists(plotsdir):
    try:
        os.makedirs(plotsdir)
    except OSError:
        pass

# read in params
pfilename = this_PSR+'/params.txt'
with open(pfilename) as pfile:
    params = [p.rstrip('\n') for p in pfile]

#####
##  POST PROCESSING
#####
#TODO what other post processing do we want?  should this be a separate script?
print "post processing for PSR: "+this_PSR+"\n"

# read in chain file and clip burn in
chain = np.loadtxt(chaindir+'/chain_1.txt')
if(args.Nburn):
    if(args.Nburn > chain.shape[0]):
        raise RuntimeError('Nburn>Nsamp, reduce Nburn')
    else:
        burn = args.Nburn
else:
    burn = int(args.burnfrac * chain.shape[0])


# strip PSR name from params
for ii, this_param in enumerate(params):
    params[ii] = this_param.replace('_'+this_PSR, '')

chain_burned=chain[burn:,:-4]

# separate params into efac, equad, jitter, other
groups = ['efac', 'equad', 'jitter']
for this_group in groups:
    print 'ploting for '+this_group
    mask = []
    for ii, this_param in enumerate(params):
        if this_group in this_param:
            mask.append(ii)
    this_names = [params[ii] for ii in mask]
    this_chain = np.array([chain_burned[:,ii] for ii in mask])
    print this_names

    # plot triangle plot for parameter group
    size = np.array([4,3]) * min(len(this_names)/2.,5)
    title = this_PSR+' -- '+this_group
    plt.rcParams['font.size'] = 6
    ax = bu.triplot(this_chain.T, labels=this_names[:],
                    title=title, tex=False, figsize=tuple(size))
    plt.savefig(plotsdir+'/'+this_group+'_tri.pdf')

# finish with other params (red noise)
print 'ploting for all others'
mask = []
for ii, this_param in enumerate(params):
    isin = False
    for this_group in groups:
        if this_group in this_param:
            isin=True
            break
    if not isin:
        mask.append(ii)
this_names = [params[ii] for ii in mask]
this_chain = np.array([chain_burned[:,ii] for ii in mask])
print this_names

# plot triangle plot for other params
size = np.array([4,3]) * min(len(this_names)/2.,5)
title=this_PSR+' -- other'
plt.rcParams['font.size'] = 6
ax = bu.triplot(this_chain.T, labels=this_names[:],
                title=title, tex=False, figsize=tuple(size))
plt.savefig(plotsdir+'/other_tri.pdf')

print "DONE"
