import sys
import builtins
import wandb
import os
import torch.distributed as dist
import torch
import socket


def suppress_print():
    """Suppresses printing from the current process."""
    def ignore(*_objects, _sep=" ", _end="\n", _file=sys.stdout, _flush=False):
        pass
    builtins.print = ignore

def suppress_wandb():
    """Suppresses wandb logging from the current_process."""
    def ignore(data, step=None, commit=None, sync=None):
        pass
    wandb.log = ignore

def init_dist(back_end="nccl"):
    """
    This function initializes the multi-gpu backend and set its rank information.
    https://pytorch.org/docs/stable/generated/torch.nn.DataParallel.html
    In PyTorch's data parallelism setting, we make a copy of the module on each device and each copy handle a split 
    of the input data. These modules communicate with each other through the master port.

    Assuming that we have 2 nodes and 4 jobs (GPUs) on each machine. We need to know the following information:
        WORLD_SIZE: the number of jobs (GPUs) in total for this run. In this case, the WORLD_SIZE is 8
        world_rank: GPU rank of the job of this task, it ranges from 0 to 7
        local_rank: GPU rank of the job within the node. Since we only have 4 tasks (GPUs), this value ranges from 0 to 3

    Parameters:
        back_end: str, by default is "nccl". 
    Return:
        local_rank: int, the local node rank id of the current job
        world_rank: int, the world node rank id of hte current job 
        WORLD_SIZE: int, the number of jobs run in parallel

    """
    WORLD_SIZE = int(os.environ["SLURM_NTASKS"])
    world_rank = int(os.environ["SLURM_PROCID"])
    local_rank = int(os.environ["SLURM_LOCALID"])
    NODELIST = os.environ['SLURM_NODELIST']
    NGPUS_PER_NODE = torch.cuda.device_count()
    HOSTNAME = socket.gethostname()
    print("Rank", world_rank, " runs on node" ,HOSTNAME, " and uses GPU", local_rank, "World SIZE", WORLD_SIZE, "NGPUS_PER_NODE", NGPUS_PER_NODE)

    dist.init_process_group(backend=back_end, rank=world_rank, world_size=WORLD_SIZE)
    print("INIT FINISHED!!!")

    # we call this function here to block the process. The script will only continue if all the jobs arrive this line. Otherwise, the job will hang
    # NOTE: never call this function wihtin the block that is only accessible to a subset of the jobs. Otherwise, the job will hang forever!
    torch.distributed.barrier()

    if world_rank != 0:
        suppress_print()
        suppress_wandb()
    return local_rank, world_rank, WORLD_SIZE

def __main__():
    local_rank, world_rank, WORLD_SIZE = init_dist(**dist_kwargs)
    # There are only 4 gpus in each node, we set our local device with local rank
    torch.cuda.set_device(local_rank)
    # we need to ensure that different data is passed on different modules. This is controlled by the random seed
    # Alternatively, we could also split the indices loaded by the dataloader (never tried that, but this should work)?
    seed = 42
    seed = int(seed) + world_rank
    torch.manual_seed(seed)

    device = torch.cuda.current_device()
    data = torch.ones([10, 10]).to(device)

    if world_rank == 0:
        for rank_recv in range(1, WORLD_SIZE):
            dist.send(tensor=data, dst=rank_recv)
            print('Rank {} sent data to rank {}'.format(0, rank_recv))
    else:
        dist.recv(tensor=data, src=0)
        print('Rank {} has received data from rank {}'.format(WORLD_RANK, 0))

