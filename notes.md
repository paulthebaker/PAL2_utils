#ERRORs encountered with PAL2 on IPTA DR2

## Jitter error
The following pulsars raise a constructPhiMatrix ERROR when running with jitter included in the model.
Simply omitting jtter seems to fix it.
Presumably these pulsars have no multiband observations.

```
J0034-0534
J0218+4232
J0437-4715
J0610-2100
J0621+1002
J0711-6830
J0751+1807
J0900-3144
J1022+1001
J1045-4509
J1721-2457
J1751-2857
J1801-1417
J1802-2124
J1804-2717
J1824-2452A
J1843-1113
J1911+1347
J2019+2425
J2033+1734
J2124-3358
J2129-5721
J2229+2643
J2322+2057
```


## Exploder Matrix error
The following pulsars raise an error when constructing the exploder matrix:

```
J1730-2304
J1911-1114
```

I haven't investigated much, and have no solution.

The full error message is:
```
Traceback (most recent call last):
  File "./PAL2_noise.py", line 28, in <module>
    model = PALmodels.PTAmodels(h5filename, pulsars=this_pulsar)
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALmodels.py", line 62, in __init__
        self.initFromFile(h5filename, pulsars=pulsars)
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALmodels.py", line 133, in initFromFile
        newpsr.readFromH5(self.h5df, psrname)
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALpsr.py", line 141, in readFromH5
        h5df.readPulsar(self, psrname)
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALdatafile.py", line 628, in readPulsar
        psr.toas, np.array(psr.flags), dt=1)
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALutils.py", line 1009, in exploderMatrixNoSingles
        bucket_ref.append([times[i], flags[i]])
```

## EFAC dimension mismatch
The following pulsars raise an error when initializing EFAC models:
```
J1600-3053
J1744-1134
```
It seems to be related to a dimensional mismatch in the `signal` vector and the `ind` mask.
`ind` is longer than `signal`.
I do not yet have a solution.

The full error message is:
```
/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALmodels.py:2584: VisibleDeprecationWarning: boolean index did not match indexed array along dimension 0; dimension is 8741 but corresponding boolean dimension is 8780
  signal['Nvec'][ind] = 0.0
Traceback (most recent call last):
    File "./PAL2_noise.py", line 37, in <module>
        model.initModel(fullmodel, memsave=True, fromFile=False, verbose=True) # trying verbose=True to see output on cluster
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALmodels.py", line 3204, in initModel
        self.addSignal(signal, index, p.Tmax)
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALmodels.py", line 2416, in addSignal
        self.addSignalEfac(signal)
    File "/home/pbaker/py_envs/pulsar/lib/python2.7/site-packages/PAL2-2015.4-py2.7.egg/PAL2/PALmodels.py", line 2584, in addSignalEfac
        signal['Nvec'][ind] = 0.0
    IndexError: index 8741 is out of bounds for axis 1 with size 8741
```
