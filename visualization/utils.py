# Description: Utility functions for visualization.

# Global Visualization Threshold constant for filtering out very small amplitudes in niche cases.
VISUALIZATION_THRESHOLD = 0.01 #1e-6

def scale_amplitude_to_size(amplitude, min_size, max_size):
    """
    Scale an amplitude (0 to 1) to a size using a linear scaling.
    
    Parameters:
        amplitude (float): The amplitude value between 0 and 1.
        min_width (float): The minimum value.
        max_width (float): The maximum value.
    
    Returns:
        float: The scaled size.
    """
    # perform linear interpolation
    return min_size + amplitude * (max_size - min_size)

def get_vertex_trace_indices(fig):
    """
    Returns all traces that starts with name 'Layer'. Used for toggling data in visualization.

    Parametrers:
        fig (): The plotly figure.

    Returns:
        Array: All vertex elements in the figure.
    """
    return [i for i, trace in enumerate(fig.data) if trace.name.startswith('Layer')]

def extract_gate_labels(data):
    """Extract gate labels from the given data. Indexes gates that appear more than once."""
    gate_labels = []
    gate_count = {}
    temp_count = {}

    # count the occurrences of each gate
    for instruction in data["gates"]:
        gate = instruction.upper()
        
        # replace "P" with Φ
        if gate == "CP":
            gate = "CΦ"
        
        if gate in gate_count:
            gate_count[gate] += 1
        else:
            gate_count[gate] = 1

    # create gate labels, indexing only those that appear more than once
    for instruction in data["gates"]:
        gate = instruction.upper()
        
        if gate == "CP":
            gate = "CΦ"
        
        # if the gate appears more than once, add an index
        if gate_count[gate] > 1:
            # increase a temporary count for gate label
            if gate in temp_count:
                temp_count[gate] += 1
            else:
                temp_count[gate] = 1
            # index the gate label
            gate_label = f"{gate}{temp_count[gate]}"
        else:
            # if the gate appears only once, use no indexing
            gate_label = gate
        
        gate_labels.append(gate_label)

    return gate_labels
