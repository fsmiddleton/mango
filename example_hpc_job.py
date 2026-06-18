"""
HPC example: read/download data from ManGO, process it, upload results back.

Prerequisites (run once on the login node):
    iron auth <username> set set.irods.icts.kuleuven.be
    module load python-irodsclient/3.2.0-GCCcore-14.2.0

Do NOT call iinit() here — the auth token from iron auth is used automatically.
"""

from irods.session import iRODSSession
from irods.meta import iRODSMeta, AVUOperation
import os
import io
import hashlib
import base64
import pandas as pd

# ── configure these for your setup ─────────────────────────────────────────
IRODS_ZONE       = "set"
COLLECTION       = f"/{IRODS_ZONE}/home/SolProp"
INPUT_FILE_NAME  = "example_data.csv"
OUTPUT_FILE_NAME = "example_results.csv"
# ───────────────────────────────────────────────────────────────────────────

env_file   = os.path.expanduser("~/.irods/irods_environment.json")
input_path = f"{COLLECTION}/{INPUT_FILE_NAME}"

# ── approach A: read directly into memory (no scratch needed) ────────────────
# Good for small/medium files. The data never touches disk on the HPC side.
print("--- Approach A: direct read ---")
with iRODSSession(irods_env_file=env_file) as session:
    obj = session.data_objects.get(input_path)
    with obj.open('r') as f:
        df = pd.read_csv(io.BytesIO(f.read()))
    print(f"Read {len(df)} rows directly from ManGO")
    print(df.head())

# ── approach B: download to $VSC_SCRATCH, then read from disk ────────────────
# Better for large files, or when you need to re-read the data multiple times
# within the same job. $VSC_SCRATCH is fast parallel storage.
print("\n--- Approach B: download to scratch ---")
scratch     = os.environ.get("VSC_SCRATCH", "/tmp")
local_input = os.path.join(scratch, INPUT_FILE_NAME)

with iRODSSession(irods_env_file=env_file) as session:
    session.data_objects.get(input_path, local_input)
    print(f"Downloaded: {input_path} -> {local_input}")

df = pd.read_csv(local_input)
print(f"Read {len(df)} rows from scratch")
print(df.head())

# ── step 2: your computation ────────────────────────────────────────────────
# Replace with your actual processing code.
# df is available from whichever approach you used above.
print("\nRunning computation...")
result_df = df.copy()  # placeholder
print("Computation done")

# ── step 3: upload results to ManGO ─────────────────────────────────────────
print("\nUploading results to ManGO...")
local_output = os.path.join(scratch, OUTPUT_FILE_NAME)
result_df.to_csv(local_output, index=False)

with iRODSSession(irods_env_file=env_file) as session:
    output_path = f"{COLLECTION}/{OUTPUT_FILE_NAME}"

    # put() does not overwrite by default — remove first if the file already exists
    try:
        session.data_objects.unlink(output_path, force=True)
        print("Removed existing output file in ManGO")
    except Exception:
        pass

    session.data_objects.put(local_output, output_path)
    print(f"Uploaded: {local_output} -> {output_path}")

    # Verify checksum
    obj = session.data_objects.get(output_path)
    algo, checksum_irods = obj.chksum().split(":", 1)
    hash_fn = hashlib.sha256()
    with open(local_output, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_fn.update(chunk)
    checksum_local = base64.b64encode(hash_fn.digest()).decode()
    if checksum_irods == checksum_local:
        print("Checksum verified: upload is complete and uncorrupted")
    else:
        print("WARNING: checksum mismatch — upload may be corrupted")

    obj.metadata.apply_atomic_operations(
        AVUOperation(operation="add", avu=iRODSMeta("produced_by", "example_hpc_job.py", "")),
        AVUOperation(operation="add", avu=iRODSMeta("slurm_job_id", os.environ.get("SLURM_JOB_ID", "unknown"), "")),
    )
    print("Metadata added")

# ── step 4: clean up scratch ────────────────────────────────────────────────
for f in [local_input, local_output]:
    try:
        os.remove(f)
    except Exception:
        pass
print("Scratch cleaned up")
print("Done")
