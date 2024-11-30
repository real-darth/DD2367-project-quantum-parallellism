from collections import defaultdict
import numpy as np
from visualization.utils import VISUALIZATION_THRESHOLD

def calculate_tw(vs_data):
    """Calculate Tw (Total Work) by summing non-zero amplitudes in all layers."""
    total_work = 0
    for layer in vs_data["layers"]:
        total_work += sum(1 for amp in layer["amplitudes"] if amp > VISUALIZATION_THRESHOLD)
    # TODO: always subtract one because of our START vertex?
    total_work -= 1
    return total_work

def calculate_tinfinity(vs_data):
    """Calculate T_infinity (Critical Path Length) using edge dependencies."""
    # build adjacency list from edges
    adjacency_list = defaultdict(list)
    for edge in vs_data["edges"]:
        start_layer, start_idx = edge["start"]
        end_layer, end_idx = edge["end"]
        adjacency_list[(start_layer, start_idx)].append((end_layer, end_idx))

    # perform DFS to find the longest path
    longest_path = defaultdict(int)

    def dfs(node):
        if node not in adjacency_list:
            return 0
        if longest_path[node]:
            return longest_path[node]
        max_length = 0
        for neighbor in adjacency_list[node]:
            max_length = max(max_length, 1 + dfs(neighbor))
        longest_path[node] = max_length
        return max_length

    # start DFS from all possible starting nodes in layer 0
    max_path_length = 0
    for layer_idx in range(len(vs_data["layers"])):
        for node_idx in range(len(vs_data["layers"][layer_idx]["amplitudes"])):
            max_path_length = max(max_path_length, dfs((layer_idx, node_idx)))

    return max_path_length
