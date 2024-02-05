# Color
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
BOLD=$(tput bold)
NORMAL=$(tput sgr0)

function red {
    printf "${RED}$@${NC}\n"
}

function green {
    printf "${GREEN}$@${NC}\n"
}

function yellow {
    printf "${YELLOW}$@${NC}\n"
}

# This should be in a pre_prompt.py hook, but atm cookiecutter has a bug related to those hooks
# We should be able to move this after everyone can use a stable version (might be a while given some people work with python 3.9)
echo -e "Do you want to use a ${BOLD}preset${NORMAL}?"
echo "This will give you the best defaults (meaning you can skip everything after the command line interface choice)."
echo -e "Options are: ${BOLD}${RED}'student'${NC}${NORMAL}, ${BOLD}${RED}'research'${NC}${NORMAL} and ${BOLD}${RED}'package'${NC}${NORMAL}:"
read preset

student="student"
research="research"
package="package"

if [ "$preset" = "$student" ] ; then
    config_name="student.yaml"
elif [ "$preset" = "$research" ] ; then
    config_name="research.yaml"
elif [ "$preset" = "$package" ] ; then
    config_name="package.yaml"
else
    config_name="default.yaml"
fi

echo -e "Do you work with conda and want to directly ${BOLD}${RED}install${NC}${NORMAL} the repo? (y/n)"
read conda

yes="y"
no="n"

if [ "$conda" = "$yes" ] ; then
    echo "Do you need a new conda env set up? (${BOLD}${RED}y${NC}${NORMAL}/${BOLD}${RED}n${NC}${NORMAL})"
    read conda_new
    if [ "$conda_new" = "$yes" ] ; then
        echo -e $(yellow "Please enter your project name")
        read name
        echo -e $(yellow "Please enter your python version")
        read version

        conda create -n $name python=$version -c conda-forge -y
        conda activate $name
        conda install gh --channel conda-forge
    else
        echo -e $(yellow "Is your conda env activated? If no, please enter the name of your env.")
        read env_name
        if [ "$env_name" = "$yes" ] ; then
            echo "Great, let's get started!"
        else
            conda activate $env_name
        fi
    fi
else
    echo "Okay, we'll skip the conda env setup."
    echo "If you have requested installation in the prompting, it's possible you'll get an error after creation."
    echo "If this happens, you don't need to worry, everything should be generated at this point."
fi

cookiecutter automl_repo_template --config-file  automl_repo_template/$config_name

