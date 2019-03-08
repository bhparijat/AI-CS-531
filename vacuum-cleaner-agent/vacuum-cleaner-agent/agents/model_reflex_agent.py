# model_reflex_agent.py
from agent import Agent
from states.action import Action
from states.percept import Percept


class ModelReflexAgent(Agent):
    """
    Model-based Reflex Agent.

    The agent saves the following states using 1 bit for each state:
    <ul>
        <li>{@code top}: If the agent's previous multiple forwards direction is top or bottom.</li>
        <li>{@code top}: If the agent took either {@code LEFT} or {@code RIGHT} turn in the previous step.</li>
        <li>{@code top}: If the agent moved forward in it's previous step.</li>
    </ul>
    """

    def __init__(self):
        self.top = True
        self.turn = False
        self.forward = False
        print("Initialized model-based reflex agent.")

    def action(self, percept):
        """
        Get the action for the corresponding input percept.
        :param percept: input percept state
        :return: action to be taken
        """

        if percept is Percept.DIRTY:
            # {@code SUCK} when {@code DIRTY}
            return Action.SUCK

        # commenting the following code because it is stopping the agent immediately because of various constraints
        # if percept is State.HOME:
        #     return random.choice([Action.FORWARD, Action.STOP])

        if percept is Percept.WALL and self.top:
            # turn {@code RIGHT} when there is wall ahead and the agent is headed top
            self.turn = True
            self.forward = False
            return Action.RIGHT

        if percept is Percept.WALL and not self.top:
            # turn {@code LEFT} when there is wall ahead and the agent is headed bottom
            self.turn = True
            self.forward = False
            return Action.LEFT

        if self.turn and not self.forward:
            self.forward = True
            return Action.FORWARD

        if self.turn and self.forward and self.top:
            # turn {@code RIGHT} when the agent took the following actions in the previous steps:
            # 1. turned in the last-to-last step
            # 2. moved {@code FORWARD}
            # 3. headed {@code TOP} in the previous to last-to-last step
            self.top = False
            self.forward = False
            return Action.RIGHT

        if self.turn and self.forward and not self.top:
            # turn {@code LEFT} when the agent took the following actions in the previous steps:
            # 1. turned in the last-to-last step
            # 2. moved {@code FORWARD}
            # 3. headed {@code BOTTOM} in the previous to last-to-last step
            self.top = True
            self.forward = False
            return Action.LEFT

        # move {@code FORWARD} in all other scenarios
        self.turn = False
        self.forward = True
        return Action.FORWARD

    def __str__(self):
        return "Model-Based Reflex Agent"
