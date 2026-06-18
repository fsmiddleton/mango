#!/bin/bash -l
#SBATCH --job-name=mango_example
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --cluster=wice
#SBATCH --partition=batch
#SBATCH --account=lp_solprop-mix
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# ── load ManGO dependencies ──────────────────────────────────────────────────
# This module provides python-irodsclient (the iRODS Python API).
module load python-irodsclient/3.2.0-GCCcore-14.2.0

# Virtual environment with pandas, tabulate, etc. (set up once with setup_venv.sh)
source $VSC_DATA/envs/mango/bin/activate

# ── sanity check: confirm auth token exists ──────────────────────────────────
# If this file is missing, run:  iron auth <username> <zone> <host>  on the login node first.
if [ ! -f "$HOME/.irods/irods_environment.json" ]; then
    echo "ERROR: ~/.irods/irods_environment.json not found."
    echo "Run 'iron auth <username> <zone> <host>' on the login node first."
    exit 1
fi

# ── run the ManGO job ────────────────────────────────────────────────────────
cd /vsc-hard-mounts/leuven-data/358/vsc35812/mango

echo "Starting ManGO job on $(hostname) at $(date)"
echo "SLURM_JOB_ID: $SLURM_JOB_ID"
echo "VSC_SCRATCH: $VSC_SCRATCH"

python example_hpc_job.py

echo "Job finished at $(date)"
