#!/bin/sh

# runs scripts to update figures
python3 data_util.py
R < winners_heatmap.R --no-save
R < winner_bars.R --no-save
