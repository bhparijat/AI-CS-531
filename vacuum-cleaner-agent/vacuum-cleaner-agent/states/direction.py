# direction.py
from state import State


class Direction(State):
    """
    Defines directions available in clock-wise direction.

    The system just add the value to get the new cell value in the related direction.
    """
    LEFT = (0, -1)
    TOP = (-1, 0)
    RIGHT = (0, 1)
    BOTTOM = (1, 0)

    def previous(self):
        """
        Get the previous direction to the current one when seen clockwise.
        :return: Next direction when rotated anti-clockwise
        """
        prev = Direction.BOTTOM
        for dir in Direction:
            if dir is self:
                return prev
            prev = dir

    def next(self):
        """
        Get the next direction to the current one when seen clockwise.
        :return: Next direction when rotated clockwise.
        """
        prev = Direction.BOTTOM
        for dir in Direction:
            if prev is self:
                return dir
            prev = dir
