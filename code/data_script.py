"""Script to gather data for Paired Moran."""
from datetime import datetime
from os import stat

import axelrod as axl
import numpy as np

# local files
import trade_strategy as ts
import paired_moran as pm
from asymmetric_game import AsymmetricGame

T = np.array(
    [
        [1, 1],
        [6, -10],
    ]
)

R = np.array(
    [
        [1, -1],
        [-3, 5],
    ]
)

trade_game = AsymmetricGame(T, R)

traders = [
    axl.Cooperator(),
    ts.CoastClear(),
    ts.Careful(),
    axl.Random(0.8),
    ts.NceBitten(5),
    axl.TitFor2Tats(),
]
regulators = [
    ts.SuspiciousForgiving(),
    ts.SuspiciousGrudge(),
    axl.Random(0.2),
    ts.Grudge(),
    ts.BudgetStretcher(),
]

winners_file = open("winners.csv", "a", encoding="utf-8")
pop_file = open("pop_per_turn.csv", "a", encoding="utf-8")

# write headers
if stat("winners.csv").st_size == 0:
    winners_file.write("time,winning_trader,winning_regulator\n")
if stat("pop_per_turn.csv").st_size == 0:
    pop_file.write("time,type,player_name,pop_per_turn\n")

try:
    while True:
        winning_trader, winning_reg, t_pop, r_pop = pm.paired_moran(traders, regulators, trade_game)
        winners_file.write(
            f"{str(datetime.now())},{winning_trader},{winning_reg}\n"
        )
        for trader in t_pop:
            pop_file.write(f"{str(datetime.now())},trader,{trader},{t_pop[trader]}\n")
        for regulator in r_pop:
            pop_file.write(f"{str(datetime.now())},regulator,{regulator},{r_pop[regulator]}\n")
        print(
            f"Completed game: {str(datetime.now())},{winning_trader},{winning_reg}"
        )
except:
    winners_file.close()
    pop_file.close()
