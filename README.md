# IMPORTANT
This is only a temporary Repository, further updates are required

# Preparation
You might need to install cookiecutter-pypackage to generate new packages 
```
conda create --name aml_apckage python=3.10
pip install pipx
pipx install cookiecutter
```

Then you can either clone this github repository and run
```
cookiecutter automl_repo_template
```

and set up everything by your own.
The template will automatically generate a new package for you.

Alternatively, you can directly generate a new package from github  

```
cookiecutter https://github.com/LUH-AI/automl_repo_template.git --checkout cookiecutter
```

# TODO List
* Add more options to `cookiecutter.json`:
  * actions to post_gen_project.py to remove unnecessary packages
* Edit template documentation (remove most of it, probably)
* merge with cluster
* test with different python versions
* make some default setups (e.g. research project, thesis, etc.) - since the cluster setup needs to run from sh anyway, we could query the config file name there