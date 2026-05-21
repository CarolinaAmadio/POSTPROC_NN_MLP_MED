# FLOAT_ASSIMILATED Pipeline

This folder contains three main Python scripts for processing assimilated float data and producing:
- `Float_assimilated_<run>.csv`
- `Float_assimilated_<run>_N3nqc.csv`
- a geographic map figure `2_fig_float_maps_dpi300_<run>.png`

## Scripts

### `0_mapfloats_assimilated.py`
- reads `*arg_mis.dat` files from an input directory
- constructs a DataFrame of assimilated float profiles for:
  - `N3n`
  - `P_l`
  - `O2o`
- writes output as:
  - `Float_assimilated_<run>.csv`

Command-line arguments:
- `-i / --inputdir` : input directory
- `-r / --namerun` : run name

### `1_map_floats_assimilated_o2_chla_n3n_recn3n.py`
- reads `Float_assimilated_<run>.csv`
- selects N3n profiles
- assigns basin membership
- writes QC output:
  - `Float_assimilated_<run>_N3nqc.csv`

Command-line arguments:
- `-i / --inputdir` : input directory
- `-r / --namerun` : run name
- `-s / --timestart` : start date in `YYYYMMDD`
- `-e / --timeend` : end date in `YYYYMMDD`

### `2_map_floats_assimilated.py`
- reads:
  - `Float_assimilated_<run>.csv`
  - `Float_assimilated_<run>_N3nqc.csv`
- generates a map of assimilated floats
- saves the figure as:
  - `2_fig_float_maps_dpi300_<run>.png`

Command-line arguments:
- `-i / --inputdir` : input directory
- `-r / --namerun` : run name

## Launcher

`Launcher.sh` runs the three scripts in sequence and sets up the Python environment and `PYTHONPATH`.

Example sequence:
```bash
python -u 0_mapfloats_assimilated.py -i $INPUTDIR -r $NAMERUN
python -u 1_map_floats_assimilated_o2_chla_n3n_recn3n.py -i $INPUTDIR -r $NAMERUN -s $TIMESTART -e $TIMEEND
python -u 2_map_floats_assimilated.py -i $INPUTDIR -r $NAMERUN
