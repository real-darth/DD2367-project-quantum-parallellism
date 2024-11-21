def CROT(prev_states, layer, amplitudes, phases, old_layer):
    """
    Visualize the CROT (Controlled Rotation) gate using precomputed phases.

    Args:
        prev_states: List of current states (indices).
        layer: Current layer index.
        amplitudes: List of amplitudes for the states.
        phases: List of precomputed phases for the states.

    Returns:
        edges: List of dictionaries representing edges with transitions, amplitudes, and phases.
    """
    edges = []

    for i in prev_states:
        # Create the edge with precomputed phase
        edge = {
            "start": (layer, i),
            "end": (layer + 1, i),
            "amplitude": amplitudes[i],
            "phase": phases[i],             # Use the precomputed phase directly
            "old_phase": old_layer["phases"][i]
        }
        edges.append(edge)

    return edges
