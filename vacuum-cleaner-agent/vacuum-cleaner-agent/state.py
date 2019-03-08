# state.py
from enum import Enum


class State(Enum):
    """
    Abstract class to define the structure of states.
    """

    def __str__(self):
        return '%5s' % str(self.name)
