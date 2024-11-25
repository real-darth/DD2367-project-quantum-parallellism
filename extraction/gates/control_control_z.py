import numpy as np

def CCZ(qubits, prev_state, layer, new_state, amplitudes, phases, threshold=1e-10):
    """
    Visualize the CCZ gate, which applies a phase flip to the target state if all control qubits are |1>.
    
    Args:
        qubits: List of qubits [control_1, control_2, ..., target].
        prev_state: Array of amplitudes from the previous state.
        layer: Current layer index in the visualization.
        new_state: Array of amplitudes after the CCZ gate.
        amplitudes: List of current amplitudes for states.
        phases: List of current phases for states.
        threshold: Minimum amplitude to consider a state significant.

    Returns:
        edges: List of dictionaries representing edges with transitions, amplitudes, and phases.
    """
    edges = []
    controls = qubits[:-1]
    target = qubits[-1]

    for i in range(len(prev_state)):
        # Determine if all control qubits are |1> for this state
        control_condition = all((i >> c) & 1 for c in controls)

        # Target state remains the same index
        target_state = i

        new_phase = phases[i] #(np.angle(prev_state[i]) + np.pi) % (2 * np.pi)  # Add a pi phase
        new_amplitude = amplitudes[i] #np.abs(prev_state[i])

        # Amplitude and phase calculation
        if control_condition and np.abs(prev_state[i]) > threshold:

            edge = {
                "start": (layer, i),
                "end": (layer + 1, target_state),
                "amplitude": new_amplitude,
                "phase": new_phase,
                "old_phase": np.angle(prev_state[i])
            }

            edges.append(edge)

        elif np.abs(prev_state[i]) > threshold:  # No condition met; state propagates
            edge = {
                "start": (layer, i),
                "end": (layer + 1, target_state),
                "amplitude": new_amplitude,
                "phase": new_phase,
                "old_phase": np.angle(prev_state[i])
            }

            edges.append(edge)

    return edges
