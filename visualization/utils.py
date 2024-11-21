def map_amplitude_to_width(amplitude, min_width=0.01, max_width=15):
    """
    Maps an amplitude (0 to 1) to a line width using a linear scaling.
    
    Parameters:
        amplitude (float): The amplitude value between 0 and 1.
        min_width (float): The minimum line width for visibility.
        max_width (float): The maximum line width.
    
    Returns:
        float: The scaled line width.
    """
    # perform linear interpolation
    return min_width + amplitude * (max_width - min_width)

def get_vertex_trace_indices(fig):
    """
    Returns all traces that starts with name 'Layer'. Used for toggling data in visualization.

    Parametrers:
        fig (): The plotly figure.

    Returns:
        Array: All vertex elements in the figure.
    """
    return [i for i, trace in enumerate(fig.data) if trace.name.startswith('Layer')]

def extract_gate_labels(vs_data):
    gate_labels = []
    gate_count = {}

    for instruction in vs_data["gates"]:
        gate = instruction.upper()
        # replace "P" with Φ for better visualization
        if gate == "CP":
            gate = "CΦ"  
        
        # track gate occurrences for indexing
        if gate in gate_count:
            gate_count[gate] += 1
        else:
            gate_count[gate] = 1

        # add indexed gate name 
        gate = f"{gate}{gate_count[gate]}"
        gate_labels.append(gate)

    return gate_labels