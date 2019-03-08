# action.py
from state import State


class Action(State):
    """
    Define different actions available.

    Can be associated with 3 bits.
    """
    SUCK = 0
    LEFT = 1
    RIGHT = 2
    FORWARD = 3
    STOP = 4
