#!/usr/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=1
#SBATCH --dependency=singleton
echo myparam: B
srun hostname
sleep 30
