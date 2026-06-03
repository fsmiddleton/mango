from mango_auth import iinit
from irods.session import iRODSSession
import os

iinit("r1130394", "set", "set.irods.icts.kuleuven.be")

env_file = os.path.expanduser('~/.irods/irods_environment.json')
with iRODSSession(irods_env_file=env_file) as session:
  (...)