#$ -cwd 
#$ -m beas
#$ -M shihuwen@mail
#$ -l h_data=32768M,h_rt=4:00:00,highp
#$ -e ./output
#$ -o ./output

#!/bin/sh

source /u/local/Modules/default/init/modules.sh
module load R

Rscript crlmm_call.r
