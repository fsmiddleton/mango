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


