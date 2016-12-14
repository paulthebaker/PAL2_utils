# PAL2_utils
Utilities for running `PAL2`.

Currently, there are only scripts to complete basic noise analysis of single pulsar TOA data.
These are a stepping stone towards further IPTA data analsyis.

## `make_hdf5.py`
Reads in tempo `.par` and `.tim` files and generates an HDF5 database for use with `PAL2`.
Needs to be run with "stripped" `.par` files, which have all of the noise parameters removed.

Currently non-general.  Assumes my (PTB's) directory path structure.

## `PAL2_ipta_noise.py`
Runs the single pulsar noise analysis.  Requires an HDF5 data file and a pulsar name.

Try
```
$ python PAL2_ipta_noise.py --help
```


## `PAL2_ipta_noise_post.py`
Generates noise parameter triangle plots for four groups of noise parameters EFAC, EQUAD, Jitter, and other.

Try
```
$ python PAL2_ipta_noise_post.py --help
```
Currently assumes a directory structure created by `PAL2_ipta_noise.py`.

# PAL2 bugs with IPTA data
PAL2 requires bandwidth flags in `.tim` files to load them with `addTempoPulsar()`.
This caused problems generating HDF5 files for use in analysis.
The simplest fix is to **comment out lines 393-402 in PALdatafile.py**.

For other runtime issues see my [notes](notes.md).

# Notes on PAL2's noise parameters
The covariance matrix for the basic white noise model is:

_**C**<sub>t t' f f'</sub>_ = _&delta;<sub>t t'</sub>_ [ _&delta;<sub>f f'</sub>_ (_F<sup>2</sup> &sigma;<sub>SNR</sub><sup>2</sup>_ + _Q<sup>2</sup>_) + _J<sup>2</sup>_]

We are separating out each time bin (TOA) and each **radio** frequency bin.
_&sigma;<sub>SNR</sub>_ is the RMS timing noise that arises from the radiometer and the template fitting process.
The RMS timing noise varies per pulsar but should be of the order microseconds (&mu;s) or better.

All of these noise sources are assumed to be uncorrelated in time, hence the _&delta;<sub>t t'</sub>_.


## EFAC
_F_ is EFAC, an _ad hoc_ multiplicative **factor** applied to _&sigma;<sub>SNR</sub>_.
If the radiometer and template fitting is accounted for correctly, this should always be 1.
Each reciever and backend system gets its own EFAC.
If a pulsar is observed by multiple observatories (_i.e._ GBT and AO), at multiple frequencies (_i.e._ 8 MHz and L-band at GBT), or the backend changes (_i.e._ GASP to GUPPI), a new EFAC paramter must be introduced.

PAL2 labels EFACs with names like:
```
efac_J1909-3744-Rcvr_800_GUPPI
efac_J1909-3744-PDFB_20CM
efac_J1909-3744-NRT.BON.2000
```
These contain info about the pulsar and instrument.


## EQUAD
_Q_ is EQUAD, summarizing any independent, excess noise that is added in **quadrature** to _&sigma;<sub>SNR</sub>_.

EQUADs should be smaller than the RMS timing noise.
PAL2 uses log<sub>10</sub>(_Q_) as its search parameter, so raw output of `-7` corresponds to 10<sup>-7</sup> sec, 100 ns.
If you find yourself looking in an unstripped `.par` file, you may notice that NANOGrav records EQUAD in units of &mu;s, while the other PTAs use the PAL2 log convention.

EQUAD uses the sam naming convention as EFAC _i.e._:
```
equad_J1909-3744-Rcvr_800_GASP
```

## ECORR / Jitter
_J_ is ECORR, noise sources that are **correlated** in radio frequency such as pulse jitter.
If a pulse is emitted earlier in the rotation phase than usual, the early TOAs will be correlated across the radio band.
Note that ECORR is outside of the _&delta;<sub>f f'</sub> term.

ECORRs should be smaller than the RMS timing noise.
PAL2 uses log<sub>10</sub>(_J_) as its search parameter, so raw output of `-7` corresponds to 10<sup>-7</sup> sec, 100 ns.
In PAL2 ECORR is keyed as `'jitter_equad'` (quadrature additive noise from jitter...) and uses flags like `incJitterEquad=True`
In the output PAL2 lavels ECORRs with names like:
'''
jitter_q_J1909-3744-Rcvr1_2_GASP
'''

In the IPTA dataset it appears only GBT and AO use simultaneous multiband observations (via the GASP/ASP, GUPPI/PUPPI backends).
Including ECORR/Jitter for pulsars not observed by GBT or AO will cause errors.


## Red Noise & DM Variations
Red Noise and DM Variations are both handled as red power spectra, parameterized by an amplitude and a spectral index, _&gamma;_.
PAL2 uses the log<sub>10</sub> amplitude and implements the spectrum as _f<sup> -&gamma;</sup>_.
A returned spectral index of `2` is a red _f<sup> -2</sup>_ spectrum.


# TODO
