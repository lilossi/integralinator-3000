#!/bin/bash
#SBATCH --job-name=integralinator-features
#SBATCH --output=/home/philippo/integralinator-3000/logs/features_%A.out
#SBATCH --error=/home/philippo/integralinator-3000/logs/features_%A.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=36:00:00

source ~/miniconda3/etc/profile.d/conda.sh
conda activate integralinator-env

REPO=/home/philippo/integralinator-3000

cd $REPO

export PYTHONUNBUFFERED=1

echo "Running feature generation"

python analysis/generate_features.py

echo "Done. Features written to analysis/features_v2.pkl and analysis/features_v2.csv"
