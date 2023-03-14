"""Function to run an asymmetric tournament."""
import axelrod as axl
import pandas as pd


def trade_tournament(traders, regulators, trade_game):
    """An asymmetrical tournament between traders and regulators."""
    matchups = [[x, y] for x in traders for y in regulators]
    outputs = []

    for matchup in matchups:
        match = axl.Match(matchup, 500, game=trade_game)
        ttotal = 0
        rtotal = 0
        for _ in range(500):
            match.play()
            tscore, rscore = match.final_score()
            ttotal += tscore
            rtotal += rscore

        outputs += [[str(matchup[0]), str(matchup[1]), ttotal / 500, rtotal / 500]]

    return pd.DataFrame(
        outputs, columns=["trader", "regulator", "trader_score", "regulator_score"]
    )
