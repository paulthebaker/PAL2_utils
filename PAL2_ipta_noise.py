#!/usr/bin/env python
from __future__ import division

import os
import argparse

from PAL2 import PALmodels
from PAL2 import PALInferencePTMCMC as ptmcmc


#####
##  ARGUMENT PARSER
#####
parser = argparse.ArgumentParser(description='run PAL2 noise analysis on IPTA pulsars')
parser.add_argument('--pulsar', action='store', required=True,
                    help='pulsar to analyze')
parser.add_argument('--hdf5', action='store', required=True,
                    help='hdf5 file containing pulsar data')
parser.add_argument('--jitter', action='store_true', required=False,
                    help='use jitter noise model')
parser.add_argument('--Nsamp', action='store', required=False, default=100000, type=int,
                    help='max number of McMC samples to collect')
parser.add_argument('--Neff', action='store', required=False, default=10000, type=int,
                    help='number of effective independent samples required to end early (estimated with acor)')

args = parser.parse_args()

h5filename = args.hdf5
this_PSR = args.pulsar
jitter = args.jitter

# generate directories for this_PSR
plotsdir = this_PSR+'/plots'
chaindir = this_PSR+'/chain'
if not os.path.exists(plotsdir):
    try:
        os.makedirs(plotsdir)
    except OSError:
        pass
if not os.path.exists(chaindir):
    try:
        os.makedirs(chaindir)
    except OSError:
        pass

print "setting up run for PSR: "+this_PSR
#####
##  Initialize Model that will include a search for:
##    Basic Noise   -- red noise (pow) + DM var (pow) + efac (default) + equad + ecorr (jitter)
##    Band Noise    --  + band noise (pow); need to determine band-binning
##    System Noise  --  + sys noise (pow); too many params, use subset of systems (most important only)
##    NonStationary --  + wavelet/shapelet; non-stationary features in red/DM noise
##    periodic DM   --  + DM Amp and spec index as sinusoid
#####
model = PALmodels.PTAmodels(h5filename, pulsars=this_PSR)

basicModel = model.makeModelDict(incRedNoise=True, noiseModel='powerlaw', nfreqs=20, 
                                 incDM=True, dmModel='powerlaw', ndmfreqs=20,
                                 incEquad=True, incJitterEquad=jitter,
                                 likfunc='mark6')

model.initModel(basicModel, memsave=True, fromFile=False, verbose=True) # trying verbose=True to see output on cluster
params = model.get_varying_parameters() # names of params for triplot labels
print 'Run Params:'
print params

with open(this_PSR+'/params.txt', 'w') as pfile: # write params to file for use in post processing
    for this_param in params:
        pfile.write("{}\n".format(this_param))

#####
##  MCMC FOR SINGLE PULSAR NOISE ANALYSIS
#####

p0 = model.initParameters()       # prior draw for starting location
cov = model.initJumpCovariance()  # cov matrix for 

lnlike = model.mark6LogLikelihood # log likelihood
lnprior = model.mark3LogPrior     # log prior

# setup sampler
# make kwarg dictionary for jitter parameter
loglkwargs = {'incJitter': jitter}

print "running sampler for PSR: "+this_PSR
sampler = ptmcmc.PTSampler(len(p0), lnlike, lnprior, cov,  outDir=chaindir,
                        loglkwargs=loglkwargs)

#####
##  RUN SAMPLER!
#####
N = args.Nsamp
Neff = args.Neff
sampler.sample(p0, N, neff=Neff, writeHotChains=True)

