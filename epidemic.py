import random
import numpy as np

def si_epidemic(graph, beta, initial_infected_count=1, max_iterations=None, max_infected_frac=1):
    """
    Simulate an SI epidemic model on a given graph.

    Parameters:
    - graph: NetworkX graph
    - beta: Probability of infection per contact
    - initial_infected_count: Number of initially infected nodes
    - max_iterations: Maximum number of iterations (None to ignore)
    - max_infected_frac: Maximum fraction of infected nodes before stopping

    Returns:
    - A list containing the infected nodes at the end of the simulation.
    """
    
    initial_infected = random.sample(list(graph.nodes()), k=initial_infected_count) # Randomly select the initial infected nodes from the graph
    infected = set(initial_infected)
    iteration = 0

    # Calculate the maximum number of infected nodes
    max_infected = None if max_infected_frac is None else int(max_infected_frac * len(graph))

    while True:
        if max_iterations is not None and iteration >= max_iterations:
            break
        if len(infected) >= max_infected:
            break

        new_infected = set()        
        infected_list = list(infected)
        random.shuffle(infected_list) # Shuffle list of infected nodes to avoid bias

        for node in infected_list:
            # Iterate over neighbors of the infected node that are not already infected
            for neighbor in set(graph.neighbors(node)) - infected:
                # Guarantee that maximum number of infected nodes is not exceeded
                if max_infected is not None and len(infected) + len(new_infected) >= max_infected:
                    break
                # With probability 'beta', attempt to infect the neighbor
                if random.random() < beta:
                    new_infected.add(neighbor) # Add the neighbor to the new infected set

        infected.update(new_infected) # Update the infected set with the newly infected nodes
        iteration += 1

    return list(infected)


def observed_infected(infected_nodes, observation_probability):
    """
    Return a list of observed infected nodes based on a given observation probability.
    
    Parameters:
    - infected_nodes: List of infected nodes.
    - observation_probability: Probability (between 0 and 1) of observing each infected node.
    
    Returns:
    - A list of observed infected nodes.
    """
    # Create an array where each element is set to the observation probability
    a = np.full(len(infected_nodes), observation_probability)
    # Generate random numbers between 0 and 1 for each infected node
    b = np.random.uniform(size=len(infected_nodes))
    # Create a mask (1 if the infected node is observed, 0 otherwise)
    c = np.multiply(b < a, 1)

    # Select the observed infected nodes
    observed_nodes = [x for x, mask in zip(infected_nodes, c) if mask==1]
    
    return observed_nodes