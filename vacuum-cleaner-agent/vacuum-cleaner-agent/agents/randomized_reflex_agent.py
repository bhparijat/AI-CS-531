# randomized_reflex_agent.py
import random

from states.percept import Percept
from states.action import Action


class RandomizedReflexAgent:
    """
    Randomized Reflex Agent
    """

    def __init__(self):
        print("Initialized randomized reflex agent.")

    def action(self, percept):
        """
        Get the action for the corresponding input percept.
        :param percept: input percept state
        :return: action to be taken
        """

        if percept is Percept.DIRTY:
            # {@code SUCK} if the percept is {@code DIRTY}
            return Action.SUCK

        # if percept is State.HOME:
        #     return Action.STOP

        if percept is Percept.WALL:
            # randomly select a turn from {@code [LEFT, RIGHT]} if the percept is {@code WALL}
            return random.choice([Action.LEFT, Action.RIGHT])

        # randomly select an action from [{@code LEFT}, {@code RIGHT}, {@code FORWARD}] in all other cases
        return random.choice([Action.LEFT, Action.RIGHT, Action.FORWARD])
