from .utils import get_vertex_trace_indices
import plotly.graph_objects as go

def add_ui_elements(fig, computational_basis, gate_labels, tw, tinfinity, show_hierarchy=False):
    num_gates = len(gate_labels)  # number of gates on the X-axis
    num_states = len(computational_basis)  # number of quantum states on the Y-axis
    
    # Calculate the aspect ratio based on the number of gates and states
    # This will ensure that the X-axis is stretched properly
    aspect_ratio = {
        'x': num_gates * 3 / (num_states),  # Control how stretched the X-axis should be
        'y': 1.2,  # Keep the Y-axis aspect ratio normal
        'z': 1   # Same for Z-axis
    }

    # Update layout for scene, basic info
    fig.update_layout(
        scene=dict(
            xaxis_title="Gate",
            xaxis=dict(
                tickvals=list(range(num_gates)),
                ticktext=gate_labels,
                range=[0, num_gates]  # Force the range of the X-axis to match number of gates
            ),
            yaxis_title="Quantum State",
            yaxis=dict(
                tickvals=list(range(num_states)),
                ticktext=computational_basis
            ),
            zaxis_title="Phase",
            aspectmode='manual',  # Use custom aspect ratio
            aspectratio=aspect_ratio  # Apply the custom aspect ratio
        ),
        title="Quantum Parallelism Visualization",
        showlegend=show_hierarchy
    )

    # Add toggle buttons for vertex text
    fig.update_layout(
        updatemenus=[{
            'buttons': [
                {
                    'args': [{"mode": ["markers"]}, get_vertex_trace_indices(fig)],
                    'label': "Hide Text",
                    'method': "restyle"
                },
                {
                    'args': [{"mode": ["markers+text"]}, get_vertex_trace_indices(fig)],
                    'label': "Show Text",
                    'method': "restyle"
                }
            ],
            'direction': "right",
            'pad': {"r": 10, "t": 10},
            'showactive': True,
            'x': 0.05,
            'xanchor': "left",
            'y': 1,
            'yanchor': "top"
        }]
    )

    # Add annotations to UI elements
    fig.update_layout(
        annotations=[
            dict(text="Vertex<br>Text", x=0, xref="paper", y=1.00,
                 yref="paper", showarrow=False),
            dict(text=f"T_w: {tw}", x=0, y=0.90, showarrow=False),
            dict(text=f"T_∞: {tinfinity}", x=0, y=0.88, showarrow=False)
        ]
    )

    # Set camera to orthographic
    fig.update_layout(
        scene=dict(
            camera=dict(
                projection=dict(type='orthographic'),   # makes depth flat
                eye=dict(x=0, y=0, z=1),                # view from above
                up=dict(x=0, y=1, z=0)                  # rotate the view 90 degrees to the right
            )
        )
    )

    return fig