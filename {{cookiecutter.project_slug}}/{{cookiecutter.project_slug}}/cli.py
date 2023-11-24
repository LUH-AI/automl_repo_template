"""Console script for {{cookiecutter.project_slug}}."""

{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
{%- endif %}
import sys
{%- if cookiecutter.command_line_interface|lower == 'click' %}
import click
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'hydra' %}
import hydra
{%- endif %}

{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}."""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
def main():
    """Console script for {{cookiecutter.project_slug}}."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "{{cookiecutter.project_slug}}.cli.main")
    return 0
{%- endif %}
{% if cookiecutter.command_line_interface|lower == 'hydra' %}
@hydra.main(version_base=None)
def main(cfg):
    """Console script for {{cookiecutter.project_slug}}."""
    print("Add arguments to this script like this:")
    print("     'python {{cookiecutter.project_slug}}/cli.py +hello=world'")
    print("Or use a yaml config file to store your arguments.")
    print("See click documentation at https://hydra.cc/docs/intro/")
    print("\n")
    print(f"Your current config is: {cfg}")
    with open("./performance.csv", "w+") as f:
        f.write("epoch,train_loss,train_acc,val_loss,val_acc\n")
        f.write("1,0.1,0.2,0.3,0.4\n")
    with open("./done.txt", "w+") as f:
        f.write("yes")
    return 0
{%- endif %}


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
