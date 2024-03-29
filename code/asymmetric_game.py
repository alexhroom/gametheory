"""Class for asymmetric games."""
from typing import Tuple, Union

import numpy as np
import axelrod as axl

C, D = axl.Action.C, axl.Action.D


class AsymmetricGame:
    """An asymmetric game that works with the Axelrod system."""

    # pylint: disable=invalid-name, too-few-public-methods
    def __init__(self, A: np.array, B: np.array) -> None:
        """
        Creates an asymmetric game which can pretend to be an Axelrod game.

        Parameters
        ----------
        A: np.array
            the payoff matrix for player A.
        B: np.array
            the payoff matrix for player B.
        """

        self.scores = {
            (C, C): (A[0][0], B[0][0]),
            (D, D): (A[1][1], B[1][1]),
            (C, D): (A[0][1], B[0][1]),
            (D, C): (A[1][0], B[1][0]),
        }

    def score(
        self, pair: Tuple[axl.Action, axl.Action]
    ) -> Tuple[Union[int, float], Union[int, float]]:
        """Returns the appropriate score for a decision pair.
        Parameters
        ----------
        pair: tuple(Action, Action)
            A pair actions for two players, for example (C, C).

        Returns
        -------
        tuple of int or float
            Scores for two player resulting from their actions.
        """
        return self.scores[pair]

    def RPST(self):
        """Returns RPST for the trader player."""
        R = self.scores[(C, C)][0]
        P = self.scores[(D, D)][0]
        S = self.scores[(C, D)][0]
        T = self.scores[(D, C)][0]
        return R, P, S, T
