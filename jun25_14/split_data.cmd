#!/bin/bash

#$ -cwd 
#$ -m beas
#$ -M shihuwen@mail
#$ -l h_data=2048M,h_rt=4:00:00
#$ -e ./output
#$ -o ./output

export PYTHONPATH=/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7/lib/python2.7/site-packages:/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7:/u/home/eeskin/shihuwen/software/ghmm/ghmm_python/lib64/python2.6/site-packages:$PYTHONPATH

source /u/local/Modules/default/init/modules.sh
module load python/2.7.3

../prep_scripts/split_train_data.py -f ../affy100k_training_data_full/affy100_hind_training_full.txt -n 40
