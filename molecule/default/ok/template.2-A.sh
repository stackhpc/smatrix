#!/usr/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=2
#SBATCH --dependency=singleton
echo myparam: A
srun hostname
sleep 30
