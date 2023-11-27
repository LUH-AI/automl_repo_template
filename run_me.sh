echo "We'll now guide you through the cluster setup and then make a new project repository for you."

echo "Will you need cluster setup (e.g. useful commands, conda installations, etc.)? (y/n)"
read cluster_setup

if [ "$cluster_setup" = "y" ];
then
    python cluster_setup.py
else
    echo "Skipping cluster setup."
fi

echo ""
echo "Now we'll let cookiecutter make a new project repository for you."
echo "It's important to have any conda environments you'll need already activated."
echo "Do you need to create a new conda environment? (y/n)"
read new_env

if [ "$new_env" = "y" ];
then
    echo "Please make and activate your conda environment and then run this script again."
    exit 1
fi

echo "Is your conda environment activated? (y/n)"
read env_activated

if [ "$env_activated" = "y" ];
then
    echo "Great! Let's get started."
else
    echo "Please activate your conda environment and then run this script again."
    exit 1
fi

echo ""
echo "Do you want to use a preset?"
echo "This will give you the best defaults (meaning you can skip everything after the command line interface choice (9/22))."
echo "Options are: 'student', 'research' and 'package'"
echo "Enter preset (or leave blank for full configuration):"
read preset

if [ "$preset" = "student" ];
then
    export COOKIECUTTER_CONFIG=automl_repo_template/student.yaml
elif [ "$preset" = "research" ];
then
    export COOKIECUTTER_CONFIG=automl_repo_template/research.yaml
elif [ "$preset" = "package" ];
then
    export COOKIECUTTER_CONFIG=automl_repo_template/package.yaml
else
    unset COOKIECUTTER_CONFIG
fi

cd ..
echo $COOKIECUTTER_CONFIG
cookiecutter automl_repo_template

echo "All done! You can now cd to your project directory. Happy coding!"