import networkx as nx

def degree(graph):
    """
    Compute the number of neighbors for all nodes, normalized by the size of the graph.

    Parameters:
    - graph: NetworkX graph
    
    Returns:
    - A dictionary with, for each node, the fraction of nodes it is connected to.
    """
    
    return nx.degree_centrality(graph)

def contact(graph, observed_nodes):
    """
    Compute the fraction of observed infected neighbors for all nodes.

    Parameters:
    - graph: NetworkX graph
    - observed_nodes: List of observed infected nodes
    
    Returns:
    - A dictionary with the fraction of observed infected neighbors for each node.
    """
    contact = {}
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        num_infected_neighbors = sum(1 for neighbor in neighbors if neighbor in observed_nodes)
        frac_infected_neighbors = num_infected_neighbors/len(neighbors) if neighbors else 0.0
        contact[node] = frac_infected_neighbors
    
    return contact

def observed_betweenness(graph, observed_nodes):
    """
    Compute the betweenness centrality of nodes considering only
    shortest paths that have both source and target nodes in the
    observed infected nodes set.

    Parameters:
    - graph: NetworkX graph
    - observed_nodes: List of observed infected nodes

    Returns:
    - A dictionary with the betweenness centrality scores.
    """

    return nx.betweenness_centrality_subset(graph, sources=observed_nodes, targets=observed_nodes)