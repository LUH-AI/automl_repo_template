#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.md')
        remove_file('docs/authors.rst')

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

    os.system(f"cd {PROJECT_DIRECTORY}")
    os.system("make install")
    os.system("pre-commit install")
    if '{{ cookiecutter.use_docs }}' != 'n':
        os.system("cd docs && make docs && cd ..")
