# ntuple-analysis
This package contains the necessary modules to produce stack histograms for an HTT analysis. 

## Environment setup
On KIT machines, in order not to have external dependencies (e.g. cvmfs) it is possible to build an own version of both Python3 and ROOT (PyROOT). This can be done in the following steps:

- assuming that anaconda is installed (if not, follow https://linuxize.com/post/how-to-install-anaconda-on-centos-7/), create a Python3.X (3.6 is tested and works, but every version of Python >= 3.5 should be fine) environment and activate it following https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/. 
- clone ROOT and build it against the newly created Python3 environment

	- ROOT >= v6.22 
	```bash
	$ /usr/bin/cmake3 -DPYTHON_EXECUTABLE=<path to virtual 	python3 environment> -Dcxxmodules="OFF" -Druntime_cxxmodules="OFF" <path to ROOT source>
	```
	- ROOT < v6.22
	```bash
	$ /usr/bin/cmake3 -Dpyroot_experimental=ON -DPYTHON_EXECUTABLE=<path to virtual 	python3 environment> -Dcxxmodules="OFF" -Druntime_cxxmodules="OFF" <path to ROOT source>
	```
- clone this repo, taking care of using the option `--recursive`
- in order to run an analysis script that includes this module from everywhere in the machine, remember to include the path to this repo to the `PYTHONPATH`
```bash
$ export PYTHONPATH=<path to local copy of ntuple-analysis>:$PYTHONPATH
```
