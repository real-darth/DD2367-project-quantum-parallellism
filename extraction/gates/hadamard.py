import numpy as np

def HAD(qubit, previous_state_data, layer, new_state, amplitudes, phases, threshold=1e-10):
    """
    Visualize the Hadamard gate, which applies a Hadamard transformation to the target qubit,
    creating superposition creating more edges, or reverting superposition collapsing edges.
    
    Args:
        qubit (tuple): Indicating which qubit is manipulated (e.g., (target_qubit,)).
        previous_state_data (list): Previous states data.
        layer (int): Current layer index.
        new_state (list): New state data.
        amplitudes (list): Precomputed amplitudes for the evolved state.
        phases (list): Precomputed phases for the evolved state.

    Returns:
        edges (list): List of dictionaries representing edges with transitions, amplitudes, and phases.
    """
    edges = []
    # extract target qubit from gate info
    target_qubit = qubit[0]
    stride = 2 ** target_qubit  # calcualte stride

    # apply the Hadamard gate to the target qubit
    for i in range(len(previous_state_data)):
        # calculate the target states after applying H
        target_zero = i  # target for |0>
        target_one = i ^ stride  # target for |1> (bit flip on target qubit with stride)

        #if np.abs(prev_state[i]) > threshold:
        #    print(f"State {i}: Amplitude {prev_state[i]} -> Targets {target_zero}, {target_one}")

        # chek if the previous state have a positive amplitude
        if np.abs(previous_state_data[i]) > threshold:
            # get the previous phase
            previous_phase = np.angle(previous_state_data[i])
            # check new target state amplitudes, make sure they have a positive amplitude
            if np.abs(new_state[target_zero]) > threshold:
                edges.append({
                    "start": (layer, i),
                    "end": (layer + 1, target_zero),
                    "amplitude": amplitudes[target_zero],
                    "phase": phases[target_zero],
                    "old_phase": previous_phase
                })
            # check other target state amplitude
            if np.abs(new_state[target_one]) > threshold:
                edges.append({
                    "start": (layer, i),
                    "end": (layer + 1, target_one),
                    "amplitude": amplitudes[target_one],
                    "phase": phases[target_one],
                    "old_phase": previous_phase
                })
    
    return edges
