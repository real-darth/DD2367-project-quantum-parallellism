def ROTATE(previous_state_index, layer, amplitudes, phases, old_layer):
    """
    Visualize any controlled phase rotation.

    Args:
        previous_state_index (list): Previous states indices.
        layer (int): Current layer index.
        amplitudes (list): Precomputed amplitudes for the evolved state.
        phases (list): Precomputed phases for the evolved state.

    Returns:
        edges (list): List of dictionaries representing edges with transitions, amplitudes, and phases.
    """
    edges = []

    for i in previous_state_index:
        # create the edge with precomputed phase
        edge = {
            "start": (layer, i),
            "end": (layer + 1, i),
            "amplitude": amplitudes[i],
            "phase": phases[i],                     # use the precomputed phase
            "old_phase": old_layer["phases"][i]     # to link the previous vertex correctly
        }
        edges.append(edge)

    return edges
