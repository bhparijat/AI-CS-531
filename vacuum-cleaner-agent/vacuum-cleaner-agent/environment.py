# environment.py
from states.action import Action
from states.percept import Percept


class Environment:
    """
    Define environment containing all it's properties and functions.
    """

    def __init__(self, name, dimensions, start_location, start_direction):
        # set properties
        self._name = name
        self._dirty_cells_count = dimensions[0] * dimensions[1]

        # define grid
        self.start_grid_state = []
        self.start_grid_state.append([Percept.WALL] * (dimensions[1] + 2))
        for r in range(dimensions[0]):
            column = [Percept.WALL]
            column.extend([Percept.DIRTY] * dimensions[0])
            column.extend([Percept.WALL])
            self.start_grid_state.append(column)
        self.start_grid_state.append([Percept.WALL] * (dimensions[1] + 2))

        # define start states
        self.start_location = start_location
        self.start_direction = start_direction

        # reset states
        self.grid_state = None
        self.location = None
        self.direction = None
        self.reset()

        print("Intialized environment.")

    @property
    def name(self):
        """
        Name of the environment.
        :return: name
        """
        return self._name

    @property
    def dirty_cells_count(self):
        """
        Count of dirty cells in the original environment.
        :return: count of dirty cells
        """
        return self._dirty_cells_count

    def add_wall(self, location):
        """
        Changes the cell states at given location from anything to {@code WALL}.
        :param location: location to add the wall
        """
        if self.start_grid_state[location[0]][location[1]] == Percept.DIRTY:
            self._dirty_cells_count = self._dirty_cells_count - 1
        self.start_grid_state[location[0]][location[1]] = Percept.WALL

    def add_door(self, location):
        """
        Changes the cell states at given location from anything to {@code CLEAN}.
        :param location: location to clean the cell
        """
        if self.start_grid_state[location[0]][location[1]] == Percept.DIRTY:
            self._dirty_cells_count = self._dirty_cells_count - 1
        self.start_grid_state[location[0]][location[1]] = Percept.CLEAN

    def reset(self):
        """
        Resets the environment to the original states.
        """
        self.grid_state = [[c for c in r] for r in self.start_grid_state]
        self.location = (self.start_location[0], self.start_location[1])
        self.direction = self.start_direction

    def percept(self):
        """
        Gets percept as seen by the agent at its location using sensors.
        :return: percept as detected by the sensors
        """
        # if the agent's current cell is {@code DIRTY}
        if self.grid_state[self.location[0]][self.location[1]] is Percept.DIRTY:
            return Percept.DIRTY

        # if the next cell the agent might move contains {@code WALL}
        new_location = tuple([self.location[i] + self.direction.value[i] for i in range(len(self.location))])
        if self.grid_state[new_location[0]][new_location[1]] is Percept.WALL:
            return Percept.WALL

        # if self.location == self.start_location:
        #     return State.HOME

        # return {@code CLEAN} in all other scenarios
        return Percept.CLEAN

    def act(self, action):
        """
        Update the environment based on the given action.
        :param action: action that needs to be applied on the environment
        """
        if action is Action.SUCK:
            self.grid_state[self.location[0]][self.location[1]] = Percept.CLEAN
        if action is Action.LEFT:
            self.direction = self.direction.previous()
        if action is Action.RIGHT:
            self.direction = self.direction.next()
        if action is Action.FORWARD:
            self.location = tuple([self.location[i] + self.direction.value[i] for i in range(len(self.location))])
        pass

    def __str__(self):
        return str('\n'.join(['   '.join([str(c) for c in r]) for r in self.grid_state]))


if __name__ == '__main__':
    dimension = (11, 11)
    location = (11, 1)
    from states.direction import Direction
    direction = Direction.TOP
    environment = Environment(dimension, location, direction)
    centroid = (6, 6)
    for ind in range(13):
        environment.add_wall((ind, centroid[1]))
        environment.add_wall((centroid[0], ind))
    doors = [(6, 1), (1, 6), (11, 6), (6, 11)]
    for door in doors:
        environment.add_door(door)
    environment.reset()
    print('Environment Info:')
    print(environment)
