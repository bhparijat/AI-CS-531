# simple_reflex_agent.py
from agent import Agent
from states.percept import Percept
from states.action import Action


class SimpleReflexAgent(Agent):
    """
    Simple Reflex Agent.
    """

    def __init__(self):
        print("Initialized simple reflex agent.")

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
            # take {@code RIGHT} turn if the percept is {@code WALL}
            return Action.RIGHT

        # move {@code FORWARD} in all other directions
        return Action.FORWARD
