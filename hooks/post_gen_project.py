#!/usr/bin/env python
import os
import io
import yaml
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    try:
        for configfile in ["../automl_repo_template/student.yaml", "../automl_repo_template/research.yaml", "../automl_repo_template/package.yaml", "../automl_repo_template/default.yaml"]:
            with open(os.path.abspath(configfile), 'r') as stream:
                config = yaml.safe_load(stream)
            if "author_full_name" not in config["default_context"].keys():
                config["default_context"]["author_full_name"] = "{{ cookiecutter.author_full_name }}"
                config["default_context"]["email"] = "{{ cookiecutter.email }}"
                config["default_context"]["github_username"] = "{{ cookiecutter.github_username }}"
                config["default_context"]["pypi_username"] = "{{ cookiecutter.pypi_username }}"
                config["default_context"]["install_dependencies_after_generation"] = "{{ cookiecutter.install_dependencies_after_generation }}"
            os.system(f"rm {configfile}")
            with io.open(configfile, 'w+', encoding='utf8') as outfile:
                yaml.dump(config, outfile, default_flow_style=False, allow_unicode=True) 
    except:
        print("Couldn't write defaults to file - moving on.")

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.md')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

    if '{{ cookiecutter.add_citation_file }}' != 'y':
        remove_file('CITATION.cff')

    if '{{ cookiecutter.use_github_workflows }}' != 'y':
        worflow_dir = os.path.join(PROJECT_DIRECTORY, ".github", "workflows")
        shutil.rmtree(worflow_dir)

    if '{{ cookiecutter.command_line_interface|lower }}' != 'hydra':
        config_dir = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', "configs")
        hydra_cluster_configs = os.path.join(config_dir, "cluster")
        hydra_base_config = os.path.join(config_dir, "base.yaml")
        shutil.rmtree(hydra_cluster_configs)
        os.remove(hydra_base_config)

        slug_dir = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}')
        hydra_utils = os.path.join(slug_dir, "hydra_utils.py")
        experiment_handling_hydra = os.path.join(slug_dir, "experiment_handling_hydra.ipynb")
        os.remove(hydra_utils)
        os.remove(experiment_handling_hydra)

    if '{{ cookiecutter.use_pyexperimenter }}' != 'y':
        config_dir = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', "configs")
        base_config = os.path.join(config_dir, "base.cfg")
        os.remove(base_config)

        slug_dir = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}')
        experiment_handling = os.path.join(slug_dir, "experiment_handling_pyexperimenter.ipynb")
        os.remove(experiment_handling)

    if '{{ cookiecutter.use_docs }}' != 'n':
        shutil.rmtree(os.path.join(PROJECT_DIRECTORY, "docs"))

    if '{{ cookiecutter.demo_code|lower }}' != 'y':
        slug = '{{ cookiecutter.project_slug }}'
        os.system(f"rm -r {PROJECT_DIRECTORY}/{slug}")
        os.system(f"mkdir {PROJECT_DIRECTORY}/{slug}")

    # Move files from cluster gen to correct location
    if os.path.exists("../automl_repo_template/cpu_example.sh"): 
        os.system("cp ../automl_repo_template/cpu_example.sh {{ cookiecutter.project_slug }}")
        os.system("cp ../automl_repo_template/gpu_example.sh {{ cookiecutter.project_slug }}")
    if os.path.exists("../automl_repo_template/PC2_infos.md"): 
        os.system("cp ../automl_repo_template/PC2_infos.md .")
    if os.path.exists("../automl_repo_template/LUIS_infos.md"): 
        os.system("cp ../automl_repo_template/LUIS_infos.md .")
    if os.path.exists("../automl_repo_template/singularity"):
        os.system("cp -r ../automl_repo_template/singularity {{ cookiecutter.project_slug }}")

    if '{{ cookiecutter.install_dependencies_after_generation }}' != 'n':
        os.system(f"cd {PROJECT_DIRECTORY}")
        exit = os.system("conda activate {{ cookiecutter.project_slug }} && make install")
        exit = os.system("conda activate {{ cookiecutter.project_slug }} && pre-commit install")
        if '{{ cookiecutter.use_docs }}' != 'n':
            os.system("cd docs && make docs && cd ..")
        os.system("git add .")
        os.system("git commit --no-verify -m 'feat: Initial commit'")
    
    print("\n")
    exit = os.system("git init -b main")
    if exit > 0:
        print("Couldn't initialize git with branch flag. Retrying with plain init.")
        os.system("git init")
    print("Do you want to push this project directly to github?")
    if input("> ") in ["y", "yes"]:
        print("Okay, we'll run the GitHub CLI for you. If you want this to be an orga repo, write the project name as 'org_name/project_name'.")
        os.system("pip install gh")
        os.system("gh repo create")
        os.system("git push --set-upstream origin main")
    
    print("\n")
    print("Great, we're done! Happy coding!")
