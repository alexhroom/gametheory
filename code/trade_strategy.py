"""File for trade-game strategies"""
import random

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

def _modify_probability(base, modifier):
    """Adds or subtracts from a variable, ensuring it's in [0, 1]"""
    if base + modifier > 1:
        return 1
    if base + modifier < 0:
        return 0
    return base + modifier

class SuspiciousGrudge(Player):
    """
    A regulator player with a 'suspicion' variable.

    'Suspicion' increases when the opponent inside trades,
    and decreases otherwise. If caught inside trading,
    the 'grudge' player will force suspicion to a high level.
    """

    name = "SuspiciousGrudge"
    classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        self.suspicion = 0.2
        super().__init__()

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        try:
            if (self.history[-1], opponent.history[-1]) == (D, D):
                self.suspicion = 1
            elif opponent.history[-1] == D:
                self.suspicion = _modify_probability(self.suspicion, 0.2)
            else:
                self.suspicion = _modify_probability(self.suspicion, -0.2)
        except IndexError:
            pass

        return self._random.random_choice(1 - self.suspicion)



class SuspiciousForgiving(Player):
    """
    A regulator player with a 'suspicion' variable.

    'Suspicion' increases when the opponent inside trades,
    and decreases otherwise. If caught inside trading,
    the 'forgiving' player will assume they won't do it again.
    """

    name = "SuspiciousForgiving"
    classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        self.suspicion = 0.2
        super().__init__()

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        try:
            if (self.history[-1], opponent.history[-1]) == (D, D):
                self.suspicion = 0.2
            elif opponent.history[-1] == D:
                self.suspicion = _modify_probability(self.suspicion, 0.2)
            else:
                self.suspicion = _modify_probability(self.suspicion, -0.2)
        except IndexError:
            pass

        return self._random.random_choice(1 - self.suspicion)


class Careful(Player):
    """
    A trader player with a 'suspicion' variable.

    This trader keeps track of the 'suspicion' variable of the
    suspicious regulator players, and inside trades inverse to
    their suspicion.
    """

    name = "Careful"
    classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        self.suspicion = 0.2
        super().__init__()

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        try:
            if (self.history[-1], opponent.history[-1]) == (D, D):
                self.suspicion = 1
            elif self.history[-1] == D:
                self.suspicion = _modify_probability(self.suspicion, 0.2)
            else:
                self.suspicion = _modify_probability(self.suspicion, -0.2)
        except IndexError:
            pass

        return self._random.random_choice(self.suspicion)

