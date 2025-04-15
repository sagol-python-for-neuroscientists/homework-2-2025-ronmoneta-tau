from collections import namedtuple
from enum import Enum
import itertools

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def apply_cure(agent: Agent) -> Agent:
    """
    Applies cure to an agent - if he is not Cure himself
    parameter agent: Agent
    return: Updated Agent
    """
    if agent.category != Condition.CURE:
        agent = Agent(agent.name, Condition(agent.category.value - 1))

    return agent


def apply_worsening(agent: Agent) -> Agent:
    """
    Applies worsening to an agent
    parameter agent: Agent
    return: Updated Agent
    """
    agent = Agent(agent.name, Condition(agent.category.value + 1))

    return agent


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    updated_agents = []

    discarded_categories = (Condition.HEALTHY, Condition.DEAD)
    ineligible = [agent for agent in agent_listing if agent.category in discarded_categories]
    eligible = [agent for agent in agent_listing if agent.category not in discarded_categories]

    for agent1, agent2 in itertools.zip_longest(*[iter(eligible)] * 2, fillvalue=None):
        # If there's an agent left without a partner, it remains unchanged.
        if agent2 is None:
            updated_agents.append(agent1)
            continue

        # handle the case when at least one agent is a Cure.
        if agent1.category == Condition.CURE or agent2.category == Condition.CURE:
            agent1 = apply_cure(agent1)
            agent2 = apply_cure(agent2)

        else:
            agent1 = apply_worsening(agent1)
            agent2 = apply_worsening(agent2)

        updated_agents.extend([agent1, agent2])

    return updated_agents + ineligible


if __name__ == '__main__':
    # Question 2
    # Copied data from tests as no actual data was provided, but wanted to adhere to the submission guidelines

    data0 = (
        Agent("Adam", Condition.SICK),
        Agent("Cure0", Condition.CURE),
        Agent("Cure1", Condition.CURE),
        Agent("Bob", Condition.HEALTHY),
        Agent("Alice", Condition.DEAD),
        Agent("Charlie", Condition.DYING),
        Agent("Vaccine", Condition.SICK),
        Agent("Darlene", Condition.DYING),
        Agent("Emma", Condition.SICK),
        Agent("Cure2", Condition.CURE),
    )
    return_value = meetup(data0)
    print(f"Question 2 solution: {return_value}")
