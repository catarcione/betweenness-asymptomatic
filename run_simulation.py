# Run simulation

import argparse
import json
import os
import random
import networkx as nx
import numpy as np

import epidemic
import centrality
import score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", type=int, required=True)
    parser.add_argument("--observation_prob", type=float, required=True)
    parser.add_argument("--max_infected_frac", type=float, required=True)
    parser.add_argument("--beta", type=float, required=True)
    parser.add_argument("--network_type", type=str, required=True)
    parser.add_argument("--initial_infected_count", type=int, default=1)
    parser.add_argument("--n_nodes", type=int, default=3000)
    parser.add_argument("--m_param", type=int, default=4)
    parser.add_argument("--k_param", type=int, default=8, help="WS: Each node is joined with its k nearest neighbors")
    parser.add_argument("--p_rewire", type=float, default=0.3, help="WS: Rewiring probability")
    parser.add_argument("--p_er", type=float, default=8/3000, help="ER: Probability for edge creation")

    parser.add_argument("--output_dir", type=str, default="results")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Generate reproducible seed
    seed = random.randint(0, 2**32 - 1)
    random.seed(seed)
    np.random.seed(seed)

    # Generate network
    if args.network_type == "ba":
        network = nx.barabasi_albert_graph(args.n_nodes, args.m_param, seed=seed)
    elif args.network_type == "ws":
        network = nx.watts_strogatz_graph(args.n_nodes, args.k_param, args.p_rewire, seed=seed)
    elif args.network_type == "er":
        network = nx.erdos_renyi_graph(args.n_nodes, args.p_er, seed=seed)
    else:
        raise ValueError(f"Unsupported network type: {args.network_type}")
    
    # Run epidemic and save infected nodes
    infected = epidemic.si_epidemic(network, args.beta, args.initial_infected_count, max_infected_frac=args.max_infected_frac)

    # Define observed infected nodes
    observed = epidemic.observed_infected(infected, args.observation_prob)

    # Compute network centrality measures
    obs_betw = centrality.observed_betweenness(network, observed)
    contact = centrality.contact(network, observed)
    degree = centrality.degree(network)

    # Compute AUC scores
    strategies = {"observed betweenness": obs_betw, "contact": contact, "degree": degree}
    score_strategies = {f"{key}": score.auc_score(infected, strategy, observed) for key, strategy in strategies.items()}
    
    # Save results
    data = {
        "seed": seed,
        "run_id": args.run_id,
        "network_type": args.network_type,
        "observation_prob": args.observation_prob,
        "max_infected_frac": args.max_infected_frac,
        "beta": args.beta,
        "aucs": score_strategies
    }

    filename = f"network_{args.network_type}_observ_prob_{args.observation_prob}_infec_frac_{args.max_infected_frac}_run{args.run_id}.json"
    filepath = os.path.join(args.output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()