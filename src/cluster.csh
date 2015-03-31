#!/bin/csh
#$ -t 1-50353
#$ -e /nfs/eecs-fserv/share/alipour/process_reps/
#$ -o /nfs/eecs-fserv/share/alipour/process_reps/
# qsub -m abe -M alipour@eecs.oregonstate.edu ddCluster.csh
#$ -N Guided-Random-testing
python /nfs/eecs-fserv/share/alipour/guided-random-testing-experiments/guided-random-testing/src/runtests.py $SGE_TASK_ID
