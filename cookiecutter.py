import os

if __name__ == '__main__': 
    # This should be in a pre_prompt.py hook, but atm cookiecutter has a bug related to those hooks
    # We should be able to move this after everyone can use a stable version (might be a while given some people work with pyhton 3.9)
    print("Do you want to use a preset?")
    print("This will give you the best defaults (meaning you can skip everything after the command line interface choice).")
    print("Options are: 'student', 'research' and 'package':")
    preset = input("> ")
    if preset == "student":
        config_name="student.yaml"
    elif preset == "research":
        config_name="research.yaml"
    elif preset == "package":
        config_name="package.yaml"
    else:
        config_name="default.yaml"
    os.system(f"cookiecutter automl_repo_template --config-file  automl_repo_template/{config_name}")