mdkir $SCRATCH/repos
mdkir $SCRATCH/envs

echo 'export ENVDIR="$SCRATCH/envs"' >> $HOME/.bashrc
echo 'export REPODIR="$SCRATCH/repos"' >> $HOME/.bashrc

sh make_conda_env.sh myenv 3.10