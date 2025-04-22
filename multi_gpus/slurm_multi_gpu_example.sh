#!/bin/bash

# the following setup works for PC2 cluster. However, this can also be adajusted to LUIS cluster.
# NOTE: The current solution only works within conda environment. However, this does not work for singularity container. 
# It seems that the slurm information cannot be properly passed within the singularity environment...

#SBATCH --ntasks-per-node=4                     # Number of tasks for each node. This value should equal to the number of GPUs (see --gres=gpu...). 
#SBATCH -N 2                                    # Number of GPU nodes. So in this script, we will apply for 2 * 4 = 8 GPUs 
#SBATCH --cpus-per-task=32                      # Number of CPUs you want on that machine (We will have 4 * 32 = 128 cpus for each node)
#SBATCH --mem 128GB                             # Amount of RAM you want (<=239GB), e.g. 64GB
#SBATCH -J SeqModel                             # Name of your job - adjust as you like
#SBATCH -A hpc-prf-intexml                      # Project name, do not change
#SBATCH -t 00:05:00                             # Timelimit of the job. See documentation for format.
#SBATCH --mail-type fail                        # Send an email, if the job fails.
#SBATCH --mail-user <y.name>@ai.uni-hannover.de               
#SBATCH --gres=gpu:a100:4                              # Number of GPUs per nodes

ml lang
module load lang/Miniforge3/24.1.2-0

conda activate conda-envs

# the following commands set up a port that allows different tasks to communicate with each other.
# If you have multiple multi-gpu jobs on the same node, then these jobs need to have different port number.
# If jobs fails with the current port number, try to use a different one.
export MASTER_PORT=12345

master_addr=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
export MASTER_ADDR=$master_addr
echo "MASTER_ADDR="$MASTER_ADDR

# we put srun here to run a parallel job
srun python -u torch_multi_gpu.py


