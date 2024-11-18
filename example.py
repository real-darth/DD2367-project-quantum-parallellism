import plotly.graph_objects as go
import numpy as np

# Example Data: Gate Layers, Qubits, Amplitudes, and Phases
# ---------------------------------------------------------
# Layers (X-axis)
layers = [0, 1, 2, 3]  # Represent gate layers
# Qubits (Y-axis)
qubits = [0, 1]  # Two qubits for simplicity
# Example connections: Each tuple is (start_layer, start_qubit, end_layer, end_qubit, amplitude, phase)
edges = [
    (0, 0, 1, 0, 0.7, 0),  # From Layer 0, Qubit 0 -> Layer 1, Qubit 0
    (0, 0, 1, 1, 0.3, np.pi/4),  # From Layer 0, Qubit 0 -> Layer 1, Qubit 1
    (1, 0, 2, 0, 0.7, np.pi/2),  # From Layer 1, Qubit 0 -> Layer 2, Qubit 0
    (1, 1, 2, 1, 0.3, np.pi),  # From Layer 1, Qubit 1 -> Layer 2, Qubit 1
    (2, 0, 3, 0, 0.7, 3*np.pi/4),  # From Layer 2, Qubit 0 -> Layer 3, Qubit 0
    (2, 1, 3, 1, 0.3, 0),  # From Layer 2, Qubit 1 -> Layer 3, Qubit 1
]

# Plotting the 3D Graph
# ---------------------------------------------------------
fig = go.Figure()

# Plot edges (connections between states)
for edge in edges:
    start_x, start_y = edge[0], edge[1]
    end_x, end_y = edge[2], edge[3]
    amplitude = edge[4]
    phase = edge[5]

    # Edge coordinates
    x = [start_x, end_x]
    y = [start_y, end_y]
    z = [np.cos(phase), np.cos(phase)]  # Z-axis encodes phase using cosine

    # Add edge with varying thickness based on amplitude
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(
            width=10 * amplitude,  # Scale amplitude for edge thickness
            color=f'rgba({int(255 * amplitude)}, 0, {int(255 * (1 - amplitude))}, 0.8)'  # Gradient color
        ),
        hoverinfo='none'
    ))

# Plot vertices (qubit states)
# ---------------------------------------------------------
# Collect unique vertices
vertices = set((edge[0], edge[1]) for edge in edges)
vertices.update((edge[2], edge[3]) for edge in edges)

for vertex in vertices:
    layer, qubit = vertex
    phase = next((edge[5] for edge in edges if edge[0] == layer and edge[1] == qubit), 0)
    fig.add_trace(go.Scatter3d(
        x=[layer], y=[qubit], z=[np.cos(phase)],
        mode='markers',
        marker=dict(size=8, color='blue'),
        name=f"Layer {layer}, Qubit {qubit}"
    ))

# Layout
fig.update_layout(
    scene=dict(
        xaxis_title="Gate Layer",
        yaxis_title="Qubit",
        zaxis_title="Phase (cosine)",
        xaxis=dict(nticks=5, range=[-0.5, 3.5]),
        yaxis=dict(nticks=5, range=[-0.5, 1.5]),
        zaxis=dict(nticks=5, range=[-1, 1]),
    ),
    title="3D Layered Graph for Quantum Parallelism",
    showlegend=False
)

# Show the graph
fig.show()
