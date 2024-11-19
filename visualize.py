import plotly.graph_objects as go
import numpy as np

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
            if (amp < 1e-6):
                continue

            label = computational_basis[state_idx]  # Use computational basis state
            fig.add_trace(go.Scatter3d(
                x=[layer_idx],  # Layer position on x-axis
                y=[state_idx],  # Computational basis state index on y-axis
                z=[phase],  # Phase value on z-axis
                mode='markers+text',
                marker=dict(size=5, color=amp, colorscale='Viridis', opacity=0.8),
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

        fig.add_trace(go.Scatter3d(
            x=[start[0], end[0]],  # Start and end layer positions on x-axis
            y=[start[1], end[1]],  # Start and end computational basis indices on y-axis
            z=[0, 0],  # Assuming phase difference shown on vertices, so edge z=0
            mode='lines',
            line=dict(width=amplitude * 5, color='blue' if phase == 0 else 'red'),  # Color by phase
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
    )

    #fig.show()
    fig.write_html("quantum" + 'plot.html', auto_open=True)


import json

def load_visualization_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Example usage
data = load_visualization_data('visualization_data.json')
visualize_quantum_parallelism(data)
