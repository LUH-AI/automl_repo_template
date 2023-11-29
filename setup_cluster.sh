yes="y"
no="n"
luis="luis"
pc2="pc2"

echo "Hi and welcome to the AutoML repo template setup!"
echo "First we'll take care of the cluster."
echo "Which cluster are you using, luis or pc2?"
read cluster

echo ""
echo "What's your username on this cluster?"
read username

echo ""
echo "Great, last question: do you want to set up conda for this cluster? (y/n)"
read conda

echo "Adding general commands to bashrc..."

echo "# Added by AutoML template" >> $HOME/.bashrc
while read -r line; do 
    echo "Adding $line to bashrc."
    echo $line >> $HOME/.bashrc; 
done < "general_bash_aliases.txt"

echo "Adding cluster-specific commands to bashrc..."

while read -r line; do 
    echo "Adding $line to bashrc."
    echo $line >> $HOME/.bashrc; 
done < "$cluster/${cluster}_bash.txt"

echo $cluster
echo [ "$cluster" = "$pc2" ]
if [ "$cluster" = "$pc2" ] ; then
    while read -r line; do
        echo "Adding $line to bashrc."
        echo $line'${username}"' >> $HOME/.bashrc;
    done < "$cluster/pc2_bash_username.txt"
fi

if [ "$cluster" = "$pc2" ] && [ "$conda" = "$yes" ] ; then
    echo "Adding conda commands to bashrc..."
    while read -r line; do 
        echo "Adding $line to bashrc."
        echo $line >> $HOME/.bashrc; 
    done < "$cluster/conda/pc2_conda_aliases.txt"
fi

if [ "$conda" = "$yes" ] ; then
    echo ""
    echo "Setting up conda, this could take a minute."
    echo "Enjoy some tea while you wait!"
    sh $cluster/conda/conda_setup.sh
    pip install pipx
    pipx install cookiecutter
fi

echo ""
echo "Now for some cleanup..."
if [ "$cluster" = "$luis" ] ; then
    rm -r "pc2"
    mv "luis/README.md" "LUIS_infos.md"
    mv "luis/cpu_example.sh" "cpu_example.sh"
    mv "luis/gpu_example.sh" "gpu_example.sh"
    rm -r "luis"
else
    rm -r "luis"
    mv "pc2/README.md" "PC2_infos.md"
    if [ "$conda" = "n" ] ; then
        echo "Are you using singularity? Here is an example of how to do that."
        mv "pc2/singularity" "."
    else
        mv "pc2/conda/cpu_example.sh" "cpu_example.sh"
        mv "pc2/conda/gpu_example.sh" "gpu_example.sh"
    fi
    rm -r "pc2"
fi

source $HOME/.bashrc
echo ""
echo "All done! You won't have to do this again, simply use the command 'make-project' to make repos from now on."
