from mango_auth import iinit
from irods.session import iRODSSession
import os
import io
import pandas as pd
from tabulate import tabulate


iinit("r1130394", "set", "set.irods.icts.kuleuven.be")

env_file = os.path.expanduser('~/.irods/irods_environment.json')
with iRODSSession(irods_env_file=env_file) as session:
    # Check what is in SolProp, a collection
    path_collection = "/set/home/SolProp"
    coll = session.collections.get(path_collection)
    # Stuff you can see about your collection 
    print(f"ID of my collection: {coll.id}")
    print(f"Name of collection: {coll.name}")
    print(f"Path of collection: {coll.path}")
    # objects in the collection 
    for obj in coll.walk():
      print(obj)

with iRODSSession(irods_env_file=env_file) as session:
    # Use the data in the example data 
    path_collection = "/set/home/SolProp"
    file_name = "example_data"
    path_data = path_collection + "/" + file_name +'.csv'
    # Get python object
    obj = session.data_objects.get(path_data)
    print('Python data object created')
    print("Metadata of the object")
    rows = []
    for item in obj.metadata.items():
        rows.append([item.name,item.value,item.units])

    print(tabulate(rows,headers=["Attribute", "Value", "Units"],tablefmt="grid"))

    # Open the file in a mode: 'r' read, 'w' write, 'append'. 
    # Not suited to large io operations but can be used on our example data !!!!!!!!!
    with obj.open('r') as f:
      data = f.read()
      print("\nHead of the object")
      print(pd.read_csv(io.BytesIO(data)).head())

    # You would instead prefer to use your data with the HPC of course..... 
    

