# agent.py


class Agent:
    """
    Abstract class to define the structure of agents.
    """

    def action(self, percept):
        """
        Get the action for the corresponding input percept.

        All agents should implement this function to return an action corresponding to the given percept.
        :param percept: input percept state
        :return: action to be taken
        """
        pass
