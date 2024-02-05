# The AutoML Project Template
This is a template you can use to get started on our research clusters and generate new project repositories with important starter code.
A quick overview of current content:

- setup script for clusters, including useful bash aliases and optional conda installation
- template for new repos with default settings for students, research papers and packages
- code quality features like linting, formating and docstring checks
- tools for improving team workflows: github actions, pre-commit, commit standards and testing
- our automl documentation setup built in
- standard plotting functions like performance over time, probability of improvement and DeepCave plots
- starter code for slurm experiment setups with hydra and PyExperimenter
- integrated tracking of emissions, time and memory 
- suggestions for quality of life features like termination handling
- integration with GitHub to push your new project to a sparkling new repo

## Using this Template
You can use this template locally as well as on LUIS or PC2. If you're working on the clusters, please start with the cluster setup - else feel free to skip to "Project Generation".

### Setting up the Cluster
Before using this template on LUIS or PC2, you should run the cluster setup script once. 
Afterwards, you can generate repos freely without touching it again.
It will provide you with some useful commands for your bashrc and make sure everything is generated in the correct places.
Additionally, if you plan on using conda on the cluster you chose, the script will install conda and its paths for you.

Start by cloning this repo. The default paths we'll use are $BIGWORK on LUIS and $SCRATCH/projects on PC2.

That means for LUIS, run:
```
cd $BIGWORK
git clone https://github.com/LUH-AI/automl_repo_template.git
cd automl_repo_template
```

And for PC2:
```
cd $PC2PFS/hpc-prf-intexml/<your-username>
mkdir projects
cd projects
git clone https://github.com/LUH-AI/automl_repo_template.git
cd automl_repo_template
```

Now you can start the cluster setup with:
```
sh setup_cluster.sh
```

You will be asked a few questions and then the script will tell you what is happening. 
Afterwards, it's a good idea to check your bashrc to make sure everything looks alright and to familiarize yourself with your new shortcuts:
```
vim $HOME/.bashrc
```
Feel free to edit the paths and aliases any way you like, but ideally you'll keep the names intact so they work the same on both clusters.

### Project Generation

You need to install the cookiecutter-pypackage to generate new packages. 
You can do this in a conda environment or even your base python. If you're not doing this in a conda environment, the generation process can generate you one afterwards:
```
pip install pipx
pipx install cookiecutter
```

This is the only dependency you'll need, so now we can get started!
There are different way of generating repos with this template:

#### Repo generation after cluster setup
This is the easiest - we gave you a shortcut to run everything required. From anywhere on the cluster, run:
```
make-project
```

#### From the cloned repo
If you want to do this locally, you can clone the github repo and give it to cookiecutter as a template path:
```
git clone https://github.com/LUH-AI/automl_repo_template.git
python automl_repo_template/cookiecutter.py
```

#### Directly generate a new package from github  
You don't need to clone the repo to use it as a template, simply provide the link to the repo. Note that this won't allow you to use templates for now:
```
cookiecutter https://github.com/LUH-AI/automl_repo_template.git --checkout cookiecutter
```

For all options, you'll be asked to provide some details on you and your new project as well as the scope of what you want.
Then, a new project will be generated. 
If you chose so, it will also be directly installed to your current python environment.
In case you opted to use documentation, that will be built as well.
Finally, we'll ask you if you want to push this local repo to a new GitHub repo as well.

## Digging into the Code
As you'll see, there are quite a few components generated for you. Here are a few suggestions of where to start:

#### If you first want to explore the code features like termination handling:
  - first go to `cli.py` in the project directory. Here you'll see how we suggest handling emission and time tracking and how your chosen command line interface is implemented.
  - then check out `<project-name>.py` - we use a function from here and also a context manager that can help us handle terminations, e.g. because of an error in the code somewhere.
  - try running your example with a few different inputs, maybe even with errors to see how the tracking and exception handling works
  - your results should include a file named `memray.bin` - this is where all the memory allocation is tracked. Run 'memray summary memray.bin' to get an idea of the memory usage (see their documentation for more options).

#### If you're mainly curious about submitting cluster jobs:
  - there are example bash scripts for the clusters that show you how single submission files can look like, it makes sense to see how this can look for you.
  - look at your bashrc: here you'll find some handy tools to check on the cluster, e.g. cluster-info or squeue-me
  - likely you'll have either chosen PyExperimenter or Hydra for this category - both come with pre-configured options for cluster deployment. Try switching from local execution to the cluster and check on your jobs!
  - the experiment_handling notebook can then help you see where which results are stored and how to load them
  - in the plotting notebook, there'll be some examples for plotting, subsitute the dummy data with your own and check how it looks. 

#### If you want to start coding right away:
  - add dependencies you'll need to `pyproject.toml`
  - add your code to `cli.py` and `<project-name>.py` in the project directory
  - write some testcases, examples and possibly documentation
  - use things like cluster examples, experiment handling and plotting if they come up, ignore or delete else

## TODO List
- test rsynch & add alias [Testing Theresa]
- re-check if deletion works for every combo of argparsing [Theresa]
- fix plotting bugs [Theresa]
- feature overview page [Caro]
  - commitzen
  - pre-commit
  - short notes for ruff & mypy
  - bump-my-version
  - memray
  - codecarbon
  - Eddy's messages
- Testing:
  - LUIS
  - Noctua [Theresa]
  - Tim Test
    - can you run what you want to run?
    - bug in generation?
    - cluster working?
    - understandable?
    - cookiecutter options meaningful?