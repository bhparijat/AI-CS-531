from matplotlib import pyplot as plt

import math

from agents.model_reflex_agent import ModelReflexAgent
from agents.randomized_reflex_agent import RandomizedReflexAgent
from agents.simple_reflex_agent import SimpleReflexAgent
from states.direction import Direction
from environment import Environment
from states.percept import Percept


def run_simple_reflex_agent(environment, iterations):
    """
    Run simple reflex agent on the given environment for given number of iterations.
    :param environment: environment the agent should act on
    :param iterations: maximum number of actions an agent can take
    """
    print(environment.name)
    print("------------------------------------------------------")
    environment.reset()
    simple_reflex_agent = SimpleReflexAgent()
    cleaned_cells_count = 0
    cleaned_cells_count_list = []
    for iteration in range(1, iterations+1):
        percept = environment.percept()
        action = simple_reflex_agent.action(percept)
        environment.act(action)

        if percept is Percept.DIRTY:
            cleaned_cells_count = cleaned_cells_count + 1
        print('[%6d] %7s %9s: %4d' % (iteration, percept, action, cleaned_cells_count))

        cleaned_cells_count_list.append(cleaned_cells_count)
    plt.plot(range(1, iterations+1), cleaned_cells_count_list, label=environment.name)
    print('Actions:', list(range(1, iterations+1)))
    print('Clean Cells:', cleaned_cells_count_list)
    print('Performance: %d' % cleaned_cells_count)
    print("------------------------------------------------------")


def run_randomized_reflex_agent(environment, epochs, iterations):
    """
    Run randomized reflex agent on the given environment for given number of iterations.
    :param environment: environment the agent should act on
    :param iterations: maximum number of actions an agent can take
    """
    # run randomized-reflex-agent
    print(environment.name)
    print("------------------------------------------------------")
    randomized_reflex_agent = RandomizedReflexAgent()
    avg_action_count_list = []
    total_action_count = 0
    for experiment in range(1, epochs+1):
        environment.reset()
        cleaned_cells_count = 0

        for iteration in range(iterations):
            percept = environment.percept()
            action = randomized_reflex_agent.action(percept)
            environment.act(action)

            if percept is Percept.DIRTY:
                cleaned_cells_count = cleaned_cells_count + 1
            print('[%6d] %7s %9s: %4d' % (iteration, percept, action, cleaned_cells_count))
            if cleaned_cells_count == 90:
                print("[Epoch: %d] Reached 90 percent performance at number of actions = %d" % (experiment, iteration))
                break

        total_action_count = total_action_count + iteration
        avg_action_count_list.append(math.ceil(1.0 * total_action_count / experiment))
        print("[Epoch: %d] performance = %d" % (experiment, 100))

    plt.plot(range(1, epochs+1), avg_action_count_list, label=environment.name)
    print('Epochs:', list(range(1, epochs+1)))
    print('Average action counts: ', avg_action_count_list)
    print("------------------------------------------------------")


def run_model_reflex_agent(environment):
    # run simple-reflex-agent
    environment.reset()
    model_reflex_agent = ModelReflexAgent()
    cleaned_cells_count = 0
    actions_count = 0
    cleaned_cells_count_list = []
    actions_count_list = []
    for iteration in range(1000):
        print('action=%d, clean=%d' % (actions_count, cleaned_cells_count))
        percept = environment.percept()
        action = model_reflex_agent.action(percept)
        environment.act(action)

        actions_count = actions_count + 1
        if percept is Percept.DIRTY:
            cleaned_cells_count = cleaned_cells_count + 1

        actions_count_list.append(actions_count)
        cleaned_cells_count_list.append(cleaned_cells_count)
    plt.plot(actions_count_list, cleaned_cells_count_list)
    plt.xlabel('Number of actions taken')
    plt.ylabel('Number of cleaned cells')
    plt.savefig('outputs/model_reflex_agent.png')
    plt.gcf().clear()
    print('Actions:', actions_count_list)
    print('Clean Cells:', cleaned_cells_count_list)
    print('Performance: %.2f' % (100.0 * cleaned_cells_count / environment.dirty_cells_count))


def run_with_first_environment():
    dimension = (10, 10)
    location = (10, 1)
    direction = Direction.TOP
    environment = Environment(dimension, location, direction)

    # run simple-reflex-agent
    run_simple_reflex_agent(environment)

    # run randomized-reflex-agent
    # run_randomized_reflex_agent(environment)

    # run states-reflex-agent
    # run_model_reflex_agent(environment)


def run_with_second_environment():
    dimension = (11, 11)
    location = (11, 1)
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

    # run simple-reflex-agent
    run_simple_reflex_agent(environment)

    # run randomized-reflex-agent
    run_randomized_reflex_agent(environment)

    # run states-reflex-agent
    run_model_reflex_agent(environment)


def run_agents():
    # definition of the first environment
    dimension1 = (10, 10)
    location1 = (10, 1)
    direction1 = Direction.TOP
    environment1 = Environment('Environment 1 (Without Walls)',  dimension1, location1, direction1)
    environment1.reset()

    # definition of the second environment
    dimension2 = (11, 11)
    location2 = (11, 1)
    direction2 = Direction.TOP
    environment2 = Environment('Environment 2 (With Walls)', dimension2, location2, direction2)
    centroid = (6, 6)
    for ind in range(13):
        environment2.add_wall((ind, centroid[1]))
        environment2.add_wall((centroid[0], ind))
    doors = [(6, 1), (1, 6), (11, 6), (6, 11)]
    for door in doors:
        environment2.add_door(door)
    environment2.reset()

    # simple reflex agent
    # print("\n\n\nRunning simple-reflex-agent")
    # print("=================================")
    # simple_reflex_agent_iterations = 80
    # run_simple_reflex_agent(environment1, simple_reflex_agent_iterations)
    # run_simple_reflex_agent(environment2, simple_reflex_agent_iterations)
    # plt.xticks([action for action in range(0, simple_reflex_agent_iterations+1, 10)])
    # plt.yticks([count for count in range(0, 41, 5)])
    # plt.xlabel('Number of actions taken')
    # plt.ylabel('Number of cleaned cells')
    # plt.legend()
    # plt.title('Simple Reflex Agent')
    # plt.savefig('outputs/simple_reflex_agent.png')
    # plt.gcf().clear()

    # randomized reflex agent
    print("\n\n\nRunning randomized-reflex-agent")
    print("=====================================")
    randomized_reflex_agent_epochs = 50
    randomized_reflex_agent_iterations = 6000
    run_randomized_reflex_agent(environment1, randomized_reflex_agent_epochs, randomized_reflex_agent_iterations)
    # run_randomized_reflex_agent(environment2, randomized_reflex_agent_epochs, randomized_reflex_agent_iterations)
    plt.xticks([epoch for epoch in range(0, randomized_reflex_agent_epochs+1, 5)])
    plt.yticks([count for count in range(2000, randomized_reflex_agent_iterations+1, 1000)])
    plt.xlabel('Number of epochs')
    plt.ylabel('Average number of actions for 100% performance')
    plt.legend()
    plt.title('Randomized Reflex Agent')
    plt.savefig('outputs/randomized_reflex_agent.png')
    plt.gcf().clear()


if __name__ == "__main__":
    plt.gcf().clear()
    run_agents()
    # run_with_first_environment()
    # run_with_second_environment()
