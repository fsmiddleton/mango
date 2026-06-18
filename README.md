# Instructions for ManGO usage 

All examples have Francesca's username (r1130394). Please replace all of these on your machine tyty. 
Creation date: 2026/06/10. 

# Using the UI 
* Navigate to [Mango](https://mango.kuleuven.be/). Login and open your zone. Click *Enter portal*.
* Open a data repository by clicking *Enter* on one. If you do not have any, contact admin to set one up for you. You'll see you can upload, copy and download data from here, as well as all the data management things including metadata creation. But we want to do it with code because we can of course. 

# Authentication  
There is a section on *How to connect* when you log in to Mango and see your active repos. The below is a repetition of some of this and could be out of date. 
## Installation
* [Install Go](https://go.dev/dl/)
* [Install iron](https://rdm-docs.icts.kuleuven.be/mango/clients/iron.html#installation). You may need to install an older version than the latest version. 

## Command line authentication 
* Open a command prompt and authenticate your machine using 
``iron auth <username> set set.irods.icts.kuleuven.be``
this is 
``iron auth <username> <zone> <host>``
* If this does not work, please connect to the VPN that allows you to connect to the server. Access instructions at [access.kuleuven.be](https://access.kuleuven.be/). I chose to connect to the VPN via https://uafw.icts.kuleuven.be/.
* You can reauthenticate with `iron auth`, without arguments, if this expires.


## Python script authentication  
* Install python libs with requirements.txt: `pip install -r requirements.txt`
* Use the `example_auth.py` script as a template to build your script to interact with Mango. 

# Managing data from your machine 
* [Documentation for python scripts](https://rdm-docs.icts.kuleuven.be/mango/clients/python_client.html)
* Please view the example py files to see how to authenticate, upload data and use data. 
* I highly recommend adding print statements and try except blocks because most of the iRODS commands do not output anything and just throw an error if something goes wrong, but you won't know which command failed unless you add print statements. 

# Using ManGO on the HPC (VSC)

Running on the KU Leuven HPC differs from a local machine in a few important ways:
* No VPN needed — you are already on the KU Leuven network.
* `iron` is pre-installed system-wide, no separate installation required.
* `python-irodsclient` is available as an environment module, no pip install needed for the core library.
* Jobs run non-interactively — you must authenticate once on the login node before submitting jobs. The auth token is then cached and picked up by your job scripts automatically.

## Authentication on the HPC

### One-time setup on the login node
Run this once (and again whenever the token expires, typically after a few days):
```bash
iron auth <username> <zone> <host>
```
Your zone and host are shown on the ManGO portal under *How to connect* when you open your data repository. For our group: `iron auth <username> set set.irods.icts.kuleuven.be`

This saves `~/.irods/irods_environment.json` and caches an auth token in `~/.irods/.irodsA`. **Re-run this before submitting jobs if it may have expired.**

### Python setup
Load the `python-irodsclient` module instead of using pip:
```bash
module load python-irodsclient/3.2.0-GCCcore-14.2.0
python -c "from irods.session import iRODSSession; print('OK')"
```

If you need additional packages (`pandas`, `mango_auth`, etc.), create a virtual environment that extends the module:
```bash
module load python-irodsclient/3.2.0-GCCcore-14.2.0
python -m venv $VSC_DATA/envs/mango --system-site-packages
source $VSC_DATA/envs/mango/bin/activate
pip install pandas tabulate mango_auth
```
Add the `module load` and `source $VSC_DATA/envs/mango/bin/activate` lines to your job scripts.

## Using ManGO in job scripts
In non-interactive job scripts, **do not call `iinit()`** — connect directly using the auth token cached by `iron auth`:
```python
from irods.session import iRODSSession
import os

env_file = os.path.expanduser('~/.irods/irods_environment.json')
with iRODSSession(irods_env_file=env_file) as session:
    # download data, compute, upload results
```
See `example_hpc_job.py` and `example_hpc_job.slurm` for a complete working example.

## Typical HPC workflow
1. Store your input data in ManGO (upload once, reuse across many jobs).
2. Authenticate: `iron auth ...` on the login node.
3. Submit your job — the script downloads data from ManGO to `$VSC_SCRATCH`, computes, and uploads results back to ManGO.
4. Find your results in ManGO without any manual file transfer.

