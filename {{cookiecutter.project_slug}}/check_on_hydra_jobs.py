import os
import shutil
import numpy as np

# TODO: add path to inner dir
data_path = os.path.abspath("results")
config_path = os.path.abspath("config.yaml")
command = "python cli.py --config-name=config arg1=10 +arg2=20"

split_command = command.split(" ")[2:]
static_args = []
sweep_args = []
for i, c in enumerate(split_command):
    if "range" in c or "," in c:
        sweep_args.append(split_command[i-1])
    else:
        static_args.append(c)

default_command = command.split(" ")[:2] + static_args
default_command = " ".join(default_command)

sweep_arg_names = []
sweep_arg_ranges = []
for s in sweep_args:
    sweep_arg_names.append(s.split("=")[0])
    if "range" in s:
        range_tuple = s.split("=")[1].split(",")
        range_tuple = range_tuple.split("(")[1][:-1]
        range_tuple = range_tuple.split(",")
        range_tuple = tuple(range_tuple[0], range_tuple[1])
        sweep_arg_ranges.append(range_tuple)
    else:
        choice_list = s.split("=")[1].split(",")
        sweep_arg_ranges.append(choice_list)

# TODO: load naming scheme from config
# TODO: revise this
for m in methods:
    missing[m] = {}
    continuing[m] = {}
    complete[m] = {}
    for c in sizes:
        missing[m][c] = {}
        continuing[m][c] = {}
        complete[m][c] = {}
        for s in seeds:
            missing[m][c][s] = []
            continuing[m][c][s] = []
            complete[m][c][s] = []
            if m == "pb2_delta_update":
                path = data_path + f"/pb2_pop_size_{c}_delta_update_seed_{s}/PPO_{env_name}/{s}"
            else:
                path = data_path + f"/{m}_pop_size_{c}_seed_{s}/PPO_{env_name}/{s}"
            final_config = path + "/final_config.yaml"
            state_path = path + "/pbt_state.pkl"
            if m == "cma":
                meth_name = "cma_pbt"
            elif m == "random":
                meth_name = "random_pbt"
            elif m == "pb2_delta_update":
                meth_name = "pb2"
            else:
                meth_name = m
            if m == "pb2_delta_update":
                runcommand = f"python exploring_pbt/run_pbt_dacbench.py -m --config-name=pb2 base_dir=results/pb2_pop_size_{c}_delta_update_seed_{s} hydra.sweeper.pbt_kwargs.population_size={c} seed={s} algo=PPO search_space=ppo env_config.env_name={env_name} +hydra.sweeper.pbt_kwargs.predict_delta=True"
            else:
                runcommand = f"python exploring_pbt/run_pbt_dacbench.py -m --config-name={meth_name} base_dir=results/{m}_pop_size_{c}_seed_{s} hydra.sweeper.pbt_kwargs.population_size={c} seed={s} algo=PPO search_space=ppo env_config.env_name={env_name}"
            if os.path.isfile(final_config):
                if os.path.exists(path+"/checkpoints"):
                    complete[m][c][s].append(path)
            elif os.path.exists(state_path):
                print(f"Method {m} size {c} seed {s} not complete.")
                logpath = path + "/pbt.log"
                iteration = 0
                with open(logpath, "r+") as f:
                    for l in f:
                        if "Generation" in l.rstrip():
                            current = int(l.split(" ")[1].split("/")[0])
                            if current > iteration:
                                iteration = current
                    
                for ckpt in os.listdir(path+"/checkpoints"):
                    if f"model_iteration_{current}" in ckpt:
                        shutil.rmtree(path+"/checkpoints/"+ ckpt)
                        pass
                continuing[m][c][s].append(runcommand+f" +hydra.sweeper.resume={state_path}")
            else:
                print(f"Method {m} size {c} seed {s} not found.")
                missing[m][c][s].append(runcommand)

all_files = []
for m in methods:
    for c in sizes:
        for s in seeds:
            filepath = f"missing_{m}_size_{c}_seed_{s}.sh"
            first = True
            for command in missing[m][c][s]+continuing[m][c][s]:
                with open(filepath, "a+") as f:
                    if first:
                        first = False
                        slurm_string = f"""#!/bin/bash \n
                        #SBATCH --error=error.err\n 
                        #SBATCH --job-name=my_job\n 
                        #SBATCH --mem=10GB\n
                        #SBATCH --output=output.out\n
                        #SBATCH --partition=ai,tnt\n 
                        #SBATCH --time=1440\n
                        conda activate my_env\n"""
                        f.write(slurm_string)
                        f.write("\n")
                    f.write(command)
                    f.write("\n")
                all_files.append(filepath)

with open("submit_all.sh", "a+") as f:
    for file in all_files:
        f.write(f"sbatch {file}")
        f.write("\n")