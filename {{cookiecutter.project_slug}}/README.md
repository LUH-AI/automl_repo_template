# {{ cookiecutter.project_name }}

{% if cookiecutter.open_source_license != 'Not open source' -%}

![https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})

![https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg](https://travis-ci.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})

![https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest](https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?version=latest)

{% if cookiecutter.add_pyup_badge == 'y' %}
![https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/)
{% endif %}

[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
{% endif %}

{{ cookiecutter.project_short_description }}

{% if cookiecutter.open_source_license != 'Not open source' -%}
- Free software: {{ cookiecutter.open_source_license }}
- Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{% endif %}

## Features

- TODO

## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
