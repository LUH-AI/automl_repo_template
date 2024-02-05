yes="y"
no="n"
luis="luis"
pc2="pc2"

echo "Hi and welcome to the AutoML repo template setup!"
echo "First we'll take care of the cluster."
echo "Which cluster are you using, luis or pc2?"
read cluster

echo ""
echo "What's your username on this cluster? (e.g. teimer for PC2)"
read username

echo "Great, let's get started!"

echo "Adding general commands to bashrc..."

echo "# >>>>>>>>>>>>>>>>>>>>>>>> AUTO ML REPO TEMPLATE" >> $HOME/.bashrc
while read -r line; do 
    echo "Adding $line to bashrc."
    echo $line >> $HOME/.bashrc; 
done < "general_bash_aliases.txt"

echo ""
echo "Adding cluster-specific commands to bashrc..."

while read -r line; do 
    echo "Adding $line to bashrc."
    echo $line >> $HOME/.bashrc; 
done < "$cluster/${cluster}_bash.txt"

if [ "$cluster" = "$pc2" ] ; then
    while read -r line; do
        echo "Adding $line${username} to bashrc."
        echo $line${username}'"' >> $HOME/.bashrc;
    done < "$cluster/pc2_bash_username.txt"
fi
echo "# <<<<<<<<<<<<<<<<<<<<<<<< AUTO ML REPO TEMPLATE" >> $HOME/.bashrc
conda init
source $HOME/.bashrc

echo ""
echo "Setting up conda..."
mkdir $REPODIR
mkdir $ENVDIR
conda-create -f environment.yml -n template
conda-activate template

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
    mv "pc2/singularity" "."
    mv "pc2/conda/cpu_example.sh" "cpu_example.sh"
    mv "pc2/conda/gpu_example.sh" "gpu_example.sh"
    rm -r "pc2"
fi

echo ""
echo "All done! You won't have to do this again on this cluster, simply use the command 'make-project' to make repos from now on."
