# percept.py
from state import State


class Percept(State):
    """
    Defines all the percepts possible.

    We need one more percept of {@code CLEAN} which is opposite of {@code DIRTY}
    because {@code not DIRTY} could mean {@WALL} or {@code CLEAN}.
    """
    WALL = 0
    DIRTY = 1
    CLEAN = 2
    HOME = 3
