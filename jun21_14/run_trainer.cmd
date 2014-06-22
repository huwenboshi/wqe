#!/bin/sh

#$ -cwd 
#$ -m beas
#$ -M shihuwen@mail
#$ -l h_data=2048M,h_rt=4:00:00,highp
#$ -e ./output
#$ -o ./output

module load python/2.7

time ./run_trainer.sh
