import itertools

observation_probs = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9]
max_infected_fracs = [0.2, 0.4, 0.6, 0.8, 0.9]
network_types = ["ba", "ws", "er"]
beta = 0.3
n_runs = 50

with open("params.txt", "w") as f:
    for observation_prob, max_infected_frac, network_type in itertools.product(observation_probs, max_infected_fracs, network_types):
        for run_id in range(n_runs):
            line = f"--run_id {run_id} --observation_prob {observation_prob} --max_infected_frac {max_infected_frac} --beta {beta} --network_type {network_type}\n"
            f.write(line)