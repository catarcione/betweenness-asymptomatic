# betweenness-asymptomatic
This repository provides the code to perform the simulations described in the paper:

**"Identifying Asymptomatic Nodes in Network Epidemics Using Betweenness Centrality"**

*Conrado C. Pinto, Daniel R. Figueiredo*

[DOI](https://doi.org/10.5753/wperformance.2024.2414)

# Overview
Asymptomatic individuals play a significant role in the spread of epidemics, yet they often remain undetected. This work proposes and evaluates methods for **identifying asymptomatic nodes** in SI (Susceptible–Infected) network-based epidemic simulations, using only the network topology and a snapshot of observed symptomatic cases.

The key contribution is a modified version of **betweenness centrality**, which considers only the shortest paths between pairs of observed infected nodes in order to rank unobserved nodes according to their likelihood of being asymptomatic.

# Modules
## `epidemic.py`
This module is responsible for **epidemic simulation** and the generation of **partial observations**.

- **`si_epidemic`** simulates an SI (Susceptible–Infected) process on a network, where infection spreads probabilistically across edges until a stopping condition is met.

- **`observed_infected`** generates a partially observed set of infected nodes by independently sampling each infected node with a given observation probability.

This module provides both the **ground-truth infected set** and its **observed subset**, which are used by the centrality-based methods and evaluation procedures.

## `centrality.py`
This module implements different **node-ranking strategies** based on network topology and observed infection data.

- **`degree`** computes the normalised degree centrality for all nodes, corresponding to the fraction of nodes to which each node is connected.

- **`contact`** computes, for each node, the fraction of its neighbours that are in the observed infected set. This captures local exposure to observed infections.

- **`observed_betweenness`** computes a modified betweenness centrality, considering only shortest paths whose endpoints are both in the observed infected set.

These measures assign a score to each node, indicating its likelihood of being infected (including asymptomatic cases). The resulting scores are later used for comparison and evaluation.

## `score.py`
This module provides evaluation metrics to assess how well different centrality-based strategies identify asymptomatic infected nodes.

- **`auc_score`** computes the **AUC (Area Under the ROC Curve)** for a given node ranking.

  The evaluation:
  - excludes observed infected nodes from the analysis,
  - treats the remaining nodes as a binary classification problem (infected vs. not infected),
  - uses centrality scores as prediction scores.

  It returns:
  - the **AUC value**, summarising ranking performance, and  
  - the **ROC curve** (FPR, TPR, thresholds) for further analysis.

This module enables quantitative comparison of different strategies by measuring how effectively they rank truly infected (but unobserved) nodes above non-infected ones.

# Contact
Questions or feedback? Please contact:
conrado@cos.ufrj.br
