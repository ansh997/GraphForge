#!/bin/bash
#SBATCH -n 16
#SBATCH --mem-per-cpu=2048
#SBATCH --time=72:00:00
#SBATCH --mincpus=8
#SBATCH --mail-user=ananth.muppidi@students.iiit.ac.in
#SBATCH --mail-type=ALL
#SBATCH --gres=gpu:1
module add cuda/12.3
module add cuda/12.2

source ~/.bashrc 
conda activate TIDL
python3 run.py

~
