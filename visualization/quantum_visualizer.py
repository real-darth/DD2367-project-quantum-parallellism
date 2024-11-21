import plotly.graph_objects as go
import numpy as np
from .utils import map_amplitude_to_width

def visualize_quantum_parallelism(data, computational_basis, fig=None):
    if fig is None:
        fig = go.Figure()

    layers = data['layers']
    edges = data['edges']

    # Add vertices for each layer
    for layer_idx, layer in enumerate(layers):
        amplitudes = layer['amplitudes']
        phases = layer['phases']

        for state_idx, (amp, phase) in enumerate(zip(amplitudes, phases)):
            if amp < 1e-6:  # Skip negligible amplitudes
                continue

            label = computational_basis[state_idx]
            fig.add_trace(go.Scatter3d(
                x=[layer_idx], 
                y=[state_idx], 
                z=[phase], 
                mode='markers',  
                marker=dict(size=5, color='black', opacity=0.8),
                text=[f"{label}<br>amp={amp:.2f}<br>phase={phase:.2f}"],
                name=f"Layer {layer_idx}"
            ))

    # Add edges
    for edge in edges:
        start, end = edge['start'], edge['end']
        amplitude, phase, old_phase = edge['amplitude'], edge['phase'], edge['old_phase']
        line_width = map_amplitude_to_width(amplitude)

        fig.add_trace(go.Scatter3d(
            x=[start[0], end[0]],  
            y=[start[1], end[1]],  
            z=[old_phase, phase],  
            opacity=amplitude,
            mode='lines',
            line=dict(width=line_width, color='blue' if phase == 0 else 'red'),  
            name=f"Edge ({start} -> {end})"
        ))

    return fig
