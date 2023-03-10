from itertools import product

import axelrod as axl
import pandas as pd
import numpy as np
from verbosemanager import VerboseManager

from asymmetric_game import AsymmetricGame

T = np.array([
    [1, 1],
    [4, -5]
    ])

R = np.array([
    [1, -1],
    [-3, 5]
    ])

trade_game = AsymmetricGame(T, R)

def trade_tournament(traders, regulators):
    """An asymmetrical tournament between traders and regulators."""
    matchups = [[x, y] for x in traders for y in regulators]
    outputs = []
    verbose_manager = VerboseManager.instance()

    verbose_manager.start(n_steps=len(matchups), verbose=3)
    for matchup in matchups:
        verbose_manager.step(str(matchup))
        match = axl.Match(matchup, 500, game=trade_game)
        ttotal = 0
        rtotal = 0
        for _ in range(500):
            match.play()
            tscore, rscore = match.final_score()
            ttotal += tscore
            rtotal += rscore

        outputs += [[matchup[0].name, matchup[1].name, ttotal/500, rtotal/500]]

    return pd.DataFrame(outputs, columns=["trader", "regulator", "trader_score", "regulator_score"])

        