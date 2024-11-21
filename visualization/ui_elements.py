from .utils import get_vertex_trace_indices

def add_ui_elements(fig, computational_basis, gate_labels, show_hierarchy=False):

    # update layout for scene, basic info
    fig.update_layout(
        scene=dict(
            xaxis_title="Gate",
            # replace with gate names
            xaxis=dict(
                tickvals=list(range(len(gate_labels))),
                ticktext=gate_labels
            ),
            yaxis_title="Quantum State",
            # replace with binary state
            yaxis=dict(
                tickvals=list(range(len(computational_basis))),
                ticktext=computational_basis
            ),
            zaxis_title="Phase",
        ),
        title="Quantum Parallelism Visualization",
        showlegend=show_hierarchy
    )

    # add toggle buttons for vertex text
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{"mode": ["markers"]}, get_vertex_trace_indices(fig)],
                        label="Hide Text",
                        method="restyle"
                    ),
                    dict(
                        args=[{"mode": ["markers+text"]}, get_vertex_trace_indices(fig)],
                        label="Show Text",
                        method="restyle"
                    )
                ]),
                direction="right",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.05,
                xanchor="left",
                y=1,
                yanchor="top"
            )
        ]
    )

    # add annotations to UI elements
    fig.update_layout(
        annotations=[
            dict(text="Vertex<br>Text", x=0, xref="paper", y=1.00,
                 yref="paper", showarrow=False)
        ]
    )

    # set camera as orthographic
    fig.update_layout(
        scene=dict(
            camera=dict(
                projection=dict(type='orthographic'),
                eye=dict(x=0, y=0, z=1)
            )
        )
    )
    return fig
