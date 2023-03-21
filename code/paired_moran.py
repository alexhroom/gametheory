"""Contains a Python implementation of the paired Moran process."""
from itertools import chain

import pandas as pd

import trade_tournament as tt

trader_players = []
regulator_players = []


def moran_step(traders: pd.Series, regulators: pd.Series, game):
    """
    Performs one step of the paired Moran process.

    Parameters
    ----------
    traders: pd.Series
        A pandas Series of trader types and their quantities.
    regulators: pd.Series
        A pandas Series of regulator types and their quantities.
    game: game
        an Axelrod game or equivalent (e.g. AsymmetricGame)
    """

    # recover lists of actual players
    # and curse at python Dicts
    # itertools.chain is used here with unpacking to flatten a list
    trader_list = list(
        chain(*[[trader_players[item[0]]] * item[1] for item in traders.items()])
    )
    regulator_list = list(
        chain(*[[regulator_players[item[0]]] * item[1] for item in regulators.items()])
    )

    data = tt.trade_tournament(trader_list, regulator_list, game)
    # trader and regulator tournament scores
    tscores = data.groupby("trader").sum("trader_score")["trader_score"]
    rscores = data.groupby("regulator").sum("regulator_score")["regulator_score"]

    def calculate_fitness(utils: pd.Series, s_quantities: pd.Series) -> pd.Series:
        """
        Calculates fitness probabilities from scores.

        Parameters
        ----------
        utils: pd.Series
            A pandas Series of utilities.
        s_quantities: pd.Series
            A pandas Series of how many of each member of the population exist.

        Returns
        -------
        A Series of fitnesses on a scale of 0 to 1, proportional to probability of reproduction.
        """
        # catches 0 weight if there's just one item
        # as otherwise rescaling gives (x - min({x})) = (x - x) = 0
        if len(utils) == 1:
            return 1

        s_rescaled = utils.apply(
            lambda x: (x - utils.min()) / (utils.max() - utils.min())
        )
        s_per_quantities = s_rescaled.mul(s_quantities)
        s_probabilities = s_per_quantities.apply(lambda x: x / s_per_quantities.sum())

        return s_probabilities

    # turn tournament scores into reproduction probabilities
    trader_fitness = calculate_fitness(tscores, traders)
    regulator_fitness = calculate_fitness(rscores, regulators)

    def birth_and_death(quantities, fitnesses):
        """Calculates and executes reproduction and death in a population."""
        death_probabilities = quantities.apply(lambda x: x / quantities.sum())

        birth_choice = quantities.sample(n=1, weights=fitnesses).keys()[0]
        death_choice = quantities.sample(n=1, weights=death_probabilities).keys()[0]

        quantities[birth_choice] += 1
        quantities[death_choice] -= 1

        return quantities

    return (
        birth_and_death(traders, trader_fitness),
        birth_and_death(regulators, regulator_fitness),
    )


def paired_moran(traders: list, regulators: list, game):
    """Runs an asymmetric paired Moran process."""

    # store name <-> player map so that pandas Series is hashable
    # pylint: disable=global-statement
    global trader_players
    trader_players = {str(trader): trader for trader in traders}
    global regulator_players
    regulator_players = {str(reg): reg for reg in regulators}

    # now turn into a Series to more easily keep track of quantities
    trader_series = pd.Series({str(t): traders.count(t) for t in traders})
    regulator_series = pd.Series({str(r): regulators.count(r) for r in regulators})

    # track population data per round for each group 
    trader_pop_data = {str(t): [1] for t in traders}
    regulator_pop_data = {str(r): [1] for r in regulators}

    timeout_ticks = 0
    while len(trader_series) > 1 or len(regulator_series) > 1:

        # timeout if hanging in a cycle
        if len(trader_series) == 1 or len(regulator_series) == 1:
            timeout_ticks += 1
            if timeout_ticks > 5:
                print("Timed out")
                # just take dominant allele and return
                trader_series = trader_series[trader_series==trader_series.max()]
                regulator_series = regulator_series[regulator_series==regulator_series.max()]
                continue

        trader_series, regulator_series = moran_step(
            trader_series, regulator_series, game
        )
        for trader in trader_series.keys():
            trader_pop_data[trader].append(trader_series[trader])

        for regulator in regulator_series.keys():
            regulator_pop_data[regulator].append(regulator_series[regulator])

        trader_series = trader_series[trader_series != 0]
        regulator_series = regulator_series[regulator_series != 0]
        print(trader_series, regulator_series)

    return trader_series.keys()[0], regulator_series.keys()[0], trader_pop_data, regulator_pop_data
