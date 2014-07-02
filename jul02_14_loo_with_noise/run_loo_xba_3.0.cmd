#!/bin/sh

#$ -cwd 
#$ -m beas
#$ -M shihuwen@mail
#$ -l h_data=2048M,h_rt=4:00:00,highp
#$ -e ./output
#$ -o ./output
#$ -t 1-10:1

i=$SGE_TASK_ID
i=$((i-1))

export PYTHONPATH=/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7/lib/python2.7/site-packages:/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7:/u/home/eeskin/shihuwen/software/ghmm/ghmm_python/lib64/python2.6/site-packages:$PYTHONPATH

source /u/local/Modules/default/init/modules.sh
module load python/2.7.3

python ../genotype_caller/run_loo.py \
    -f ../affy100k_training_data_noise_3.0/affy100_xba_training_noise_3.0.txt.$i \
    -o ./loo_out_xba_3.0/loo_out_xba_3.0.$i \
    -a 1 -b 10000 -c 100 -d 2 -e 1.0
