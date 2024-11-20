import plotly.graph_objects as go
import numpy as np

# Configuration booleans
SHOW_VERTEX_TEXT = True  # Toggle text on/off for vertices
SHOW_HIERARCHY = False  # Toggle the legend (hierarchy on the right)

def visualize_quantum_parallelism(data):
    layers = data['layers']
    edges = data['edges']

    # Dynamically generate computational basis states
    num_states = max(len(layer['amplitudes']) for layer in layers)  # Find max number of states
    computational_basis = [f"|{bin(i)[2:].zfill(int(np.log2(num_states)))}⟩" for i in range(num_states)]

    # Prepare Plotly figure
    fig = go.Figure()

    # Add vertices for each layer
    for layer_idx, layer in enumerate(layers):
        amplitudes = layer['amplitudes']
        phases = layer['phases']

        for state_idx, (amp, phase) in enumerate(zip(amplitudes, phases)):
            #print(f"Amplitude: {amp}, Phase: {phase}")
            # hide amplitudes that are near zero for now...
            if (amp < 1e-6):
                continue

            label = computational_basis[state_idx]  # Use computational basis state
            fig.add_trace(go.Scatter3d(
                x=[layer_idx],  # Layer position on x-axis
                y=[state_idx],  # Computational basis state index on y-axis
                z=[phase],  # Phase value on z-axis

                mode='markers'+ ('+text' if SHOW_VERTEX_TEXT else ''),
                marker=dict(size=5, color='black', opacity=0.8),
                text=[f"{label}<br>amp={amp:.2f}<br>phase={phase:.2f}"],
                textposition="top center",
                name=f"Layer {layer_idx}"
            ))

    # Add edges
    for edge in edges:
        start = edge['start']
        end = edge['end']
        amplitude = edge['amplitude']
        phase = edge['phase']
        old_phase = edge['old_phase']

        # Map amplitude to line thickness (closer to 1 means thicker)
        line_width = map_amplitude_to_width(amplitude)

        fig.add_trace(go.Scatter3d(
            x=[start[0], end[0]],  # Start and end layer positions on x-axis
            y=[start[1], end[1]],  # Start and end computational basis indices on y-axis

            # TODO: Fix so it gets the previous phase value to link
            z=[old_phase, phase],
            mode='lines',
            line=dict(width=line_width, color='blue' if phase == 0 else 'red'),  # Color by phase
            name=f"Edge ({start} -> {end})"
        ))

    # Customize layout
    fig.update_layout(
        scene=dict(
            xaxis_title="Layer (Gate)",
            yaxis_title="Quantum State",
            yaxis=dict(tickvals=list(range(len(computational_basis))),
                       ticktext=computational_basis),
            zaxis_title="Phase",
        ),
        title="Quantum Parallelism Visualization",
        showlegend=SHOW_HIERARCHY  # Toggle hierarchy visibility
    )

    fig.write_html("quantum" + 'plot.html', auto_open=True)


def map_amplitude_to_width(amplitude, min_width=0.001, max_width=10):
    """
    Maps an amplitude (0 to 1) to a line width using a linear scaling.
    
    Parameters:
        amplitude (float): The amplitude value between 0 and 1.
        min_width (float): The minimum line width for visibility.
        max_width (float): The maximum line width.
    
    Returns:
        float: The scaled line width.
    """
    # Ensure amplitude stays in the range [0, 1]
    amplitude = max(0, min(1, amplitude))
    
    # Perform linear interpolation
    return min_width + amplitude * (max_width - min_width)



import json

def load_visualization_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Example usage
data = load_visualization_data('visualization_data.json')
visualize_quantum_parallelism(data)
