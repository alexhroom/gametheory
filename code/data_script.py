"""Script to gather data for Paired Moran."""
from datetime import datetime

import axelrod as axl
import numpy as np

# local files
import trade_tournament as tt
import trade_strategy as ts
import paired_moran as pm
from asymmetric_game import AsymmetricGame

T = np.array([
    [1, 1],
    [6, -10]
    ])

R = np.array([
    [1, -1],
    [-3, 5]
    ])

trade_game = AsymmetricGame(T, R)

traders = [axl.Cooperator(), axl.TitFor2Tats(), ts.Careful(), axl.Random(0.75), ts.NceBitten(1), ts.NceBitten(5)]
regulators = [ts.SuspiciousForgiving(), ts.SuspiciousGrudge(), axl.Random(0.5), axl.Random(0.2), ts.Grudge()]

file = open("results.csv", 'a')
try:
    while True:
        file.write("Hello world!")
        winning_trader, winning_reg = pm.paired_moran(traders, regulators, trade_game)
        file.write(f"{str(datetime.now()),winning_trader.keys()[0],winning_reg.keys()[0]}")
except:
    file.close()