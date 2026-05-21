#! /bin/bash

#SBATCH --job-name=DA_FLOAT
#SBATCH -N1
#SBATCH --ntasks-per-node=16
#SBATCH --time=00:20:00
#SBATCH --mem=100gb
#SBATCH --account=OGS_test2528
#SBATCH --partition=g100_meteo_prod
#SBATCH --qos=qos_meteo


export ONLINE_REPO=/g100_work/OGS_test2528/V13C/QUID/SETUP/PREPROC/FLOATS/ONLINE
INPUTDIR="/g100_scratch/userexternal/gbolzon0/V13C/QUID/wrkdir/DA/"
NAMERUN='DA_SAT_FLOAT_V13C_QUID'
TIMESTART='20220101'
TIMEEND='20250101'

source /g100_work/OGS23_PRACE_IT/COPERNICUS/py_env_3.9.18_new/bin/activate
export PYTHONPATH=/g100_scratch/userexternal/camadio0/V13C/bit.sea/src/

#python -u 0_mapfloats_assimilated.py -i $INPUTDIR -r $NAMERUN

#python -u 1_map_floats_assimilated_o2_chla_n3n_recn3n.py -r $NAMERUN -s $TIMESTART -e $TIMEEND
python -u 2_map_floats_assimilated.py -i $INPUTDIR -r $NAMERUN



