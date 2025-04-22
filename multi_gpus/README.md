# Multi GPU setup

This scripts shows you how to submit jobs on slurm with multiple GPUs. Additionally, we also provide a small example on how to run data parallelism on the cluster.

TODO List:
* Model saving and Loading (In principle, save and load should work on rank 0. However, once the rank 0 loads the weights, it needs to spread the loaded weights to the other ranks)
* [FSDP](https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html), when the model is too large to fit into one gpu, we need to split them into mulitple GPUs. 
* ...

Some useful resources:
* The Ultra-Scale Playbook from Huggingface: https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=data_parallelism
* TorchTune receipes. This contains multiple examples on FSDP training/fine-tuning: https://github.com/pytorch/torchtune/tree/main/recipes
* nanogpt on ddp setting: https://github.com/karpathy/nanoGPT/blob/master/train.py
