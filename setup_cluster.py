import sys
import os
import shutil
from typing import Any, Dict

options: Dict[str, Any] = {
    "features": {
        "init": {
            "default": True,
            "prompt": "Do you need to set up the cluster for the first time?",
            "help": (
                "Will add the default bashrc entries and set up conda if applicable."
            ),
        },
        "conda": {
            "default": True,
            "prompt": "Do you want to set up conda?",
            "help": (
                "This is only necessary if you want to use conda and have not done so before on this cluster."
            ),
        },
        "new-env": {
            "default": True,
            "prompt": "Do you want to create a new conda environment for this repo?",
        },
    },
    "params": {
        "cluster": {
            "default": "luis",
            "prompt": "Which cluster do you want to use, luis or pc2? (default: luis)",
        },
        "username": {
            "default": None,
            "prompt": "What is you cluster username?",
        },
        "env-name": {
            "default": None,
            "prompt": "What is the name of your (existing or new) conda environment (if applicable)?",
        },
        "python-version": {
            "default": "3.11",
            "prompt": "Which python version do you want to use? (default: 3.11)",
        },
    },
}

infos = {}
for p in options["params"]:
    print(p["prompt"])
    val = input("> ")
    if val not in ["", "\n", None]:
        valid = True
    elif p["default"] is not None:
        val = p["default"]
    infos[p] = val

print(f"These are the details you chose: {infos}")
print("Is this correct? [y/n]")
if input("> ") in ["n", "no"]:
    print("Please try again and enter the correct details.")
    sys.exit(1)

todos = {}
for p in options["features"]:
    print(p["prompt"])
    val = input("> ")
    if val not in ["", "\n", None]:
        valid = True
    elif p["default"] is not None:
        val = p["default"]
    todos[p] = val

if infos["cluster"] == "luis":
    source_path = "luis"
else:
    source_path = "pc2"

print("\n")
if todos["init"]:
    print("Adding general commands to bashrc...")
    with open("general_bash_aliases.txt", "r") as f:
        for line in f:
            print(line)
            os.system(f"echo {line} >> $HOME/.bashrc")
    if infos["cluster"] == "pc2":
        print("Adding global PC2 aliases to bashrc...")
        with open(f"{source_path}/pc2_bash_paths.txt", "r") as f:
            for line in f:
                path = line.strip()+f'{infos["username"]}"'
                print(path)
                os.system(f"echo {path} >> $HOME/.bashrc")
        if todos["conda"]:
            print("Adding conda aliases to bashrc...")
            with open(f"{source_path}/conda/pc2_conda_aliases.txt", "r") as f:
                for line in f:
                    print(line)
                    os.system(f"echo {line} >> $HOME/.bashrc")
    else:
        print("Adding global LUIS aliases to bashrc...")
        with open(f"{source_path}/luis_bash.txt", "r") as f:
            for line in f:
                path = line.strip()+f'{infos["username"]}"'
                print(path)
                os.system(f"echo {path} >> $HOME/.bashrc")
print("\n")

if todos["conda"]:
    os.system(f"sh {source_path}/conda_setup/setup_conda.sh")

if todos["new-env"]:
    os.system(f"sh {source_path}/conda_setup/make_conda_env.sh {infos['env-name']} {infos['python-version']}")

if infos["cluster"] == "luis":
    shutil.rmtree("pc2")
    shutil.move("luis/README.md", "LUIS_infos.md")
    shutil.move("luis/cpu_example.sh", "cpu_example.sh")
    shutil.move("luis/gpu_example.sh", "gpu_example.sh")
    shutil.rmtree("luis")
else:
    shutil.rmtree("luis")
    shutil.move("pc2/README.md", "PC2_infos.md")
    if not todos["conda"] and not todos["new-env"]:
        print("Are you using singularity? Here is an example of how to do that.")
        file_names = os.listdir("pc2/singularity")
        for file_name in file_names:
            shutil.move(os.path.join("pc2/singularity", file_name), ".")
    else:
        shutil.move("pc2/conda/cpu_example.sh", "cpu_example.sh")
        shutil.move("pc2/conda/gpu_example.sh", "gpu_example.sh")
    shutil.rmtree("pc2")

print("Done!")

