import plotly.graph_objects as go
import numpy as np

def visualize_quantum_parallelism(data):
    """
    Visualize quantum parallelism as a 3D layered graph using Plotly.
    
    Args:
        data (dict): Contains information about layers, amplitudes, phases, and edges.
    """
    fig = go.Figure()

    # Plot edges (connections between layers)
    for edge in data["edges"]:
        start_layer, start_qubit = edge["start"]
        end_layer, end_qubit = edge["end"]
        amplitude = edge["amplitude"]
        phase = edge["phase"]

        # Define coordinates
        x = [start_layer, end_layer]
        y = [start_qubit, end_qubit]
        z = [0, phase]  # Z-axis encodes phase

        # Add the edge as a line
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(
                width=10 * amplitude,  # Edge thickness proportional to amplitude
                color=f'rgba(0, 100, 200, {amplitude})'  # Blue edges with alpha as amplitude
            ),
            hoverinfo='none'
        ))

    # Plot vertices (states at each layer)
    for layer_data in data["layers"]:
        layer = layer_data["layer"]
        amplitudes = layer_data["amplitudes"]
        phases = layer_data["phases"]

        for qubit, (amplitude, phase) in enumerate(zip(amplitudes, phases)):
            if amplitude > 1e-6:  # Ignore negligible states
                fig.add_trace(go.Scatter3d(
                    x=[layer], y=[qubit], z=[phase],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=f'rgba(255, 0, 0, {amplitude})'  # Red vertices, alpha for amplitude
                    ),
                    name=f"Layer {layer}, Qubit {qubit}"
                ))

    # Layout and styling
    fig.update_layout(
        scene=dict(
            xaxis_title="Gate Layer",
            yaxis_title="Qubit",
            zaxis_title="Phase",
            xaxis=dict(nticks=5, range=[-0.5, len(data["layers"]) + 0.5]),
            yaxis=dict(nticks=5, range=[-0.5, 2]),  # Assuming max 2 qubits here
            zaxis=dict(nticks=5, range=[-np.pi, np.pi]),  # Range of phases
        ),
        title="Quantum Parallelism Visualization",
        showlegend=False
    )

    # Show the graph
    fig.show()


import json

def load_visualization_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Example usage
data = load_visualization_data('visualization_data.json')
visualize_quantum_parallelism(data)
