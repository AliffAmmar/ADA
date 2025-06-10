# Part 4: The Broken Stargate - Pathfinding with Custom Weights

import pandas as pd
import networkx as nx

# Load the dataset (update the path as needed)
file_path = "/Users/A/Downloads/Dataset for Group Project-20250605/Stargate_Data.csv"

df = pd.read_csv(file_path)

# Create a directed graph
G = nx.DiGraph()

# Define custom weights
time_weight = 0.4
energy_weight = 0.3
risk_weight = 0.3

# Add edges with custom cost
for index, row in df.iterrows():
    from_node = row['From']
    to_node = row['To']
    time = row['Time']
    energy = row['Energy']
    risk = row['Risk']

    cost = (time_weight * time) + (energy_weight * energy) + (risk_weight * risk)

    G.add_edge(from_node, to_node,
               time=time, energy=energy, risk=risk, cost=cost)

# Define start and end gates
start_gate = "Gate-01"
end_gate = "Gate-20"

# Find the shortest path using the custom cost as weight
try:
    shortest_path = nx.dijkstra_path(G, start_gate, end_gate, weight='cost')
    total_cost = nx.dijkstra_path_length(G, start_gate, end_gate, weight='cost')

    print("Optimal Path from", start_gate, "to", end_gate, ":")
    print(" -> ".join(shortest_path))
    print(f"\nTotal Combined Cost: {total_cost:.2f}")

    # Optional: Print segment costs
    print("\nSegment Breakdown:")
    for i in range(len(shortest_path) - 1):
        u, v = shortest_path[i], shortest_path[i + 1]
        edge = G[u][v]
        print(f"{u} -> {v} | Time: {edge['time']} | Energy: {edge['energy']} | Risk: {edge['risk']} | Cost: {edge['cost']:.2f}")

except nx.NetworkXNoPath:
    print(f"No path found from {start_gate} to {end_gate}.")
