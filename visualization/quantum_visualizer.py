import plotly.graph_objects as go
import numpy as np
from .utils import scale_amplitude_to_size
from .utils import VISUALIZATION_THRESHOLD

VERTEX_MIN_SIZE = 1.6
VERTEX_MAX_SIZE = 7
LINE_MIN_SIZE = 0.01
LINE_MAX_SIZE = 15

def visualize_quantum_parallelism(data, computational_basis, fig=None):
    if fig is None:
        fig = go.Figure()

    layers = data['layers']
    edges = data['edges']

    # add vertices for each layer
    for layer_idx, layer in enumerate(layers):
        amplitudes = layer['amplitudes']
        phases = layer['phases']

        for state_idx, (amp, phase) in enumerate(zip(amplitudes, phases)):
            if amp < VISUALIZATION_THRESHOLD:   # skip negligible amplitudes
                continue

            label = computational_basis[state_idx]
            fig.add_trace(go.Scatter3d(
                x=[layer_idx],
                y=[state_idx],
                z=[phase],
                mode='markers',
                marker=dict(size=scale_amplitude_to_size(amp, VERTEX_MIN_SIZE, VERTEX_MAX_SIZE), color='black', opacity=0.8),
                text=[f"{label}<br>amp={amp:.2f}<br>phase={phase:.2f}"],
                name=f"Layer {layer_idx}"
            ))

    # add edges
    for edge in edges:
        start, end = edge['start'], edge['end']
        amplitude, phase, old_phase = edge['amplitude'], edge['phase'], edge['old_phase']
        line_width = scale_amplitude_to_size(amplitude, LINE_MIN_SIZE, LINE_MAX_SIZE)

        fig.add_trace(go.Scatter3d(
            x=[start[0], end[0]],
            y=[start[1], end[1]],
            z=[old_phase, phase],
            opacity=np.clip(amplitude+.07, 0, 1),   # limit value in range 0 to 1
            mode='lines',
            line=dict(width=line_width, color='blue' if phase == 0 else 'red'),  
            name=f"Edge ({start} -> {end})"
        ))

    return fig
