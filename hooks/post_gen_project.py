#!/usr/bin/env python
import os

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

    if '{{ cookiecutter.use_pyexperimenter }}' != "y":
        plotting_file = os.path.join('{{ cookiecutter.project_slug }}', 'plotting_example_pyexperimenter.py')
        remove_file(plotting_file)
        if 'hydra' not in '{{ cookiecutter.command_line_interface|lower }}':
            plotting_file = os.path.join('{{ cookiecutter.project_slug }}', 'plotting_example_hydra.py')
            remove_file(plotting_file)
            old_path = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', 'plotting_example_generic.py')
            new_path = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', 'plotting_example.py')
            os.rename(old_path, new_path)
        else:
            plotting_file = os.path.join('{{ cookiecutter.project_slug }}', 'plotting_example_generic.py')
            remove_file(plotting_file)
            old_path = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', 'plotting_example_hydra.py')
            new_path = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', 'plotting_example.py')
            os.rename(old_path, new_path)
    else:
        old_path = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', 'plotting_example_pyexperimenter.py')
        new_path = os.path.join(PROJECT_DIRECTORY, '{{ cookiecutter.project_slug }}', 'plotting_example.py')
        os.rename(old_path, new_path)
        plotting_file_hydra = os.path.join('{{ cookiecutter.project_slug }}', 'plotting_example_hydra.py')
        plotting_file_generic = os.path.join('{{ cookiecutter.project_slug }}', 'plotting_example_generic.py')
        remove_file(plotting_file_hydra)
        remove_file(plotting_file_generic)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

    # TODO add options to remove github actions
