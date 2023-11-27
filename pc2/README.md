# PC2 Cluster

## Getting Access
For information on how to setup the access to the PC2 cluster, please check the [docs](https://docs.google.com/document/d/1BavfcqX6hdbElOb3xKcTOLKhutgzKWCfk1WIh1lh12Y/edit?usp=sharing).



* example sbatch file
* option to use singularity or standard conda environment
* alias for typical folders



## Workflow as bash commands
Adjust your variables in `workflows/variable.sh`.
To clone your repo and install the environment, run `bash workflows/install.sh`.
To activate your env, run `bash workflows/activate.sh`.

Other useful commands:
```bash
# start interactive job in tmux
salloc --time=1:00:00 --nodes=1 --ntasks=16 --mem-per-cpu=4G

# Sync your files 
rsync -av --delete source target

``` 

## Debugging on the cluster / Using the cluster as a code server
If you use Visual Studio Code, you can remote into the cluster.
For this you need to setup an extra ssh config to properly configure the ssh proxy jumps.
You can find the necessary ssh configs [here](https://upb-pc2.atlassian.net/wiki/spaces/PC2DOK/pages/1902225/Access+for+Applications+like+Visual+Studio+Code).
