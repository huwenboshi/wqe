#!/bin/sh

#$ -cwd 
#$ -m beas
#$ -M shihuwen@mail
#$ -l h_data=2048M,h_rt=4:00:00,highp
#$ -e ./output
#$ -o ./output
#$ -t 1-40:1

i=$SGE_TASK_ID
i=$((i-1))

export PYTHONPATH=/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7/lib/python2.7/site-packages:/u/home/s/shihuwen/project/wqe/software/cvxopt-1.1.7:/u/home/eeskin/shihuwen/software/ghmm/ghmm_python/lib64/python2.6/site-packages:$PYTHONPATH

source /u/local/Modules/default/init/modules.sh
module load python/2.7.3

python ../genotype_caller/run_loo.py \
    -f ../affy100k_training_data_full/affy100_hind_training_full.txt.$i \
    -o ./loo_out_4/loo_out_4.$i \
    -a 1 -b 10 -c 40 -d 30 -e 2.5
