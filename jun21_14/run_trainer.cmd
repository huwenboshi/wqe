#!/bin/sh

#$ -cwd 
#$ -m beas
#$ -M shihuwen@mail
#$ -l h_data=2048M,h_rt=4:00:00,highp
#$ -e ./output
#$ -o ./output

export PYTHONPATH=/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7/lib/python2.7/site-packages:/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7:/u/home/eeskin/shihuwen/software/ghmm/ghmm_python/lib64/python2.6/site-packages:$PYTHONPATH

module load python/2.7

time ./run_trainer.sh
