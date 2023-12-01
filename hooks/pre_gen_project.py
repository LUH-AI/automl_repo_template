import os
import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_slug}}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project slug (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)

    #Exit to cancel project
    sys.exit(1)

if __name__ == '__main__':
    print("Welcome to the project generation script.")
    print("We'll now make you a new project repository.")
    print("\n")

    print("Do you work with conda and want to directly install the repo?")
    if input("> ") in ["y", "yes"]:
        print("Do you need a new conda env set up?")
        if input("> ") in ["y", "yes"]:
            exit = os.system("conda-create -n {{cookiecutter.project_slug}} python={{cookiecutter.python_version}} -c conda-forge -y")
            if exit != 0:
                exit = os.system("conda create -n {{cookiecutter.project_slug}} python={{cookiecutter.python_version}} -c conda-forge -y")
                os.system("conda activate {{ cookiecutter.project_slug }} && conda install gh --channel conda-forge")
            else:
                os.system("conda-activate {{ cookiecutter.project_slug }} && conda install gh --channel conda-forge")
        else:
            print("Is your conda env activated? If no, please enter the name of your env.")
            env_name = input("> ")
            if env_name in ["y", "yes"]:
                print("Great, let's get started!")
            else:
                exit = os.system(f"conda-activate {env_name}")
                if exit != 0:
                    exit = os.system(f"conda activate {env_name}")
    else:
        print("Okay, we'll skip the conda env setup.")
        print("If you have requested installation in the prompting, it's possible you'll get an error after creation.")
        print("If this happens, you don't need to worry, everything should be generated at this point.")
    print("\n")
