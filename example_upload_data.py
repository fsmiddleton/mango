
from mango_auth import iinit
from irods.session import iRODSSession
import os
from irods.meta import iRODSMeta, AVUOperation
import hashlib
import base64

iinit("r1130394", "set", "set.irods.icts.kuleuven.be")

env_file = os.path.expanduser('~/.irods/irods_environment.json')
with iRODSSession(irods_env_file=env_file) as session:
    # set path variables for this file 
    path_collection = "/set/home/SolProp"
    local_path = "example_data.csv"
    file_name = "example_data"
    path_data = path_collection + "/" + file_name +'.csv'
    # First check my collection exists
    try:
        coll = session.collections.get(path_collection)
        print('Collection exists')
    except: 
        # create a new collection 
        coll = session.collections.create(path_collection)
        print(' New collection created')

    # upload some data to your collection
    # session.data_objects.put(local_path, path_collection)
    print('Data uploaded')
    # get the python object describing this data 
    obj = session.data_objects.get(path_data)

    # add some metadata because you're a good engineer who cares about data lineage 
    obj.metadata.apply_atomic_operations(
        AVUOperation(operation='add', avu=iRODSMeta('key', 'Unique record identifier', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solute_smiles', 'The SMILES representation of the solute', '')),
        AVUOperation(operation='add', avu=iRODSMeta('Temperature', 'Experimental temperature', 'K')),
        AVUOperation(operation='add', avu=iRODSMeta('Solubility', 'Solubility of the solute', 'mole fraction')),
        AVUOperation(operation='add', avu=iRODSMeta('LogS', 'Logarithm of solubility', 'log(mole fraction)')),
        AVUOperation(operation='add', avu=iRODSMeta('Solubility', 'Solubility expressed as grams per 100 grams solvent', 'g/100g')),
        AVUOperation(operation='add', avu=iRODSMeta('LogS', 'Logarithm of solubility in g/100g solvent', 'log(g/100g)')),
        AVUOperation(operation='add', avu=iRODSMeta('Solvent1', 'Primary solvent name', '')),
        AVUOperation(operation='add', avu=iRODSMeta('Solvent2', 'Secondary solvent name', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent1_smiles', 'SMILES representation of solvent 1', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent2_smiles', 'SMILES representation of solvent 2', '')),
        AVUOperation(operation='add', avu=iRODSMeta('Fraction_Solvent1', 'Fraction of solvent 1 in solvent mixture', 'fraction')),
        AVUOperation(operation='add', avu=iRODSMeta('Fraction_Type', 'Type of fraction representation used', '')),
        AVUOperation(operation='add', avu=iRODSMeta('Compound_Name', 'Common or chemical name of the solute compound', '')),
        AVUOperation(operation='add', avu=iRODSMeta('CAS', 'CAS registry number of the solute', '')),
        AVUOperation(operation='add', avu=iRODSMeta('PubChem_CID', 'PubChem Compound Identifier', '')),
        AVUOperation(operation='add', avu=iRODSMeta('FDA_Approved', 'Indicates whether the compound is FDA approved', 'boolean')),
        AVUOperation(operation='add', avu=iRODSMeta('Source', 'Source or reference of the experimental data', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solute_inchi', 'InChI representation of the solute', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent1_inchi', 'InChI representation of solvent 1', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent2_inchi', 'InChI representation of solvent 2', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solute_MW', 'Molecular weight of the solute', 'g/mol')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent1_MW', 'Molecular weight of solvent 1', 'g/mol')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent2_MW', 'Molecular weight of solvent 2', 'g/mol')),
        AVUOperation(operation='add', avu=iRODSMeta('temperature', 'Experimental temperature', 'K')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent1_density', 'Density of solvent 1', 'g/cm^3')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent2_density', 'Density of solvent 2', 'g/cm^3')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent1_density_warning', 'Warning flag for solvent 1 density value', 'boolean')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent2_density_warning', 'Warning flag for solvent 2 density value', 'boolean')),
        AVUOperation(operation='add', avu=iRODSMeta('fraction_mole', 'Mole fraction of solvent component', 'mole fraction')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent_avg_density', 'Average density of solvent mixture', 'g/cm^3')),
        AVUOperation(operation='add', avu=iRODSMeta('solute_smiles_canonical', 'Canonical SMILES representation of the solute', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent1_smiles_canonical', 'Canonical SMILES representation of solvent 1', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent2_smiles_canonical', 'Canonical SMILES representation of solvent 2', '')),
        AVUOperation(operation='add', avu=iRODSMeta('logS', 'Calculated or normalized logarithmic solubility', 'log(mole fraction)')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent_density', 'Density of solvent or solvent mixture', 'g/cm^3')),
        AVUOperation(operation='add', avu=iRODSMeta('molefrac', 'Mole fraction', 'mole fraction')),
        AVUOperation(operation='add', avu=iRODSMeta('MP_pred', 'Predicted melting point of the solute', 'K')),
        AVUOperation(operation='add', avu=iRODSMeta('MP_std', 'Standard deviation of melting point prediction', 'K')),
        AVUOperation(operation='add', avu=iRODSMeta('logS_calc', 'Calculated logarithmic solubility', 'log(mole fraction)')),
        AVUOperation(operation='add', avu=iRODSMeta('gamma', 'Activity coefficient', 'dimensionless')),
        AVUOperation(operation='add', avu=iRODSMeta('solute_inchi_std', 'Standardized InChI representation of the solute', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent1_inchi_std', 'Standardized InChI representation of solvent 1', '')),
        AVUOperation(operation='add', avu=iRODSMeta('solvent2_inchi_std', 'Standardized InChI representation of solvent 2', '')),
        AVUOperation(operation='add', avu=iRODSMeta('count_p', 'Count of positive charges or protonation sites', 'count')),
        AVUOperation(operation='add', avu=iRODSMeta('count_q', 'Count of charges or ionization states', 'count')),
        AVUOperation(operation='add', avu=iRODSMeta('has_point_in_inchi', 'Indicates whether InChI contains disconnected components', 'boolean')),
        AVUOperation(operation='add', avu=iRODSMeta('has_charge', 'Indicates whether the molecule carries a formal charge', 'boolean'))
    )
    print('Metadata added')
    
    # Print properties of the object uploaded 
    print(f"ID of the object: {obj.id}")
    print(f"Name of the object: {obj.name}")
    print(f"Path of the object: {obj.path}")
    print(f"Size of the object: {obj.size}")
    # You can also find the checksum of the file, which is used to ensure it uploaded completely and without corruption 
    
    checksum = obj.chksum()
    algo, checksum_irods = checksum.split(':', 1)
    print(f"Checksum of the data using the {algo} hash algorithm: {checksum_irods}")
    #  Compare to the csv hash 
    hash = hashlib.sha256()

    with open('example_data.csv', 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash.update(chunk)

    checksum_local = base64.b64encode(hash.digest()).decode()
    if checksum_irods == checksum_local:
        print("File uploaded correctly")
    else: 
        print("Error in upload, checksums do not match")

    print('End')