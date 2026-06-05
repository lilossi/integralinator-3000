#!/bin/bash
#SBATCH --job-name=integralinator
#SBATCH --output=/home/philippo/integralinator-3000/logs/run_%A_%a.out
#SBATCH --error=/home/philippo/integralinator-3000/logs/run_%A_%a.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=36:00:00
#SBATCH --array=0-0

source ~/miniconda3/etc/profile.d/conda.sh
conda activate integralinator-env

REPO=/home/philippo/integralinator-3000
OUTDIR=$REPO/outputs
mkdir -p $OUTDIR

cd $REPO

export PYTHONUNBUFFERED=1

METHODS=(genetic)
COUNTS=(1000)

METHOD=${METHODS[$SLURM_ARRAY_TASK_ID]}
COUNT=${COUNTS[$SLURM_ARRAY_TASK_ID]}

OUTFILE=$OUTDIR/${METHOD}_${COUNT}.txt

echo "Running method=$METHOD num_integrals=$COUNT"

python -m cli.main generate --method $METHOD --num-integrals $COUNT > $OUTFILE 2>&1

echo "Done. Output written to $OUTFILE"
