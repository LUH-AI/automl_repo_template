#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

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
        worflow_dir = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', "configs")
        shutil.rmtree(worflow_dir)

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

    if '{{ cookiecutter.install_after_generation }}' != 'n':
        os.system(f"cd {PROJECT_DIRECTORY}")
        os.system("make install")
        os.system("git init -b main")
        os.system("pre-commit install")
        if '{{ cookiecutter.use_docs }}' != 'n':
            os.system("cd docs && make docs && cd ..")
        os.system("git add .")
        os.system("git commit --no-verify -m 'feat: Initial commit'")
    
    print("\n")
    print("Do you want to push this project directly to github?")
    if input("> ") in ["y", "yes"]:
        print("Okay, we'll run the GitHub CLI for you. If you want this to be an orga repo, write the project name as 'org_name/project_name'.")
        os.system("gh repo create")
        os.system("git push --set-upstream origin main")
    
    print("\n")
    print("Great, we're done! Happy coding!")
