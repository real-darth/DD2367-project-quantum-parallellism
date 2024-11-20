import numpy as np

def HAD(qubit, prev_states, num_states, layer, new_layer, old_layer):
    edges = []
    
    # get the qubit being manipulated
    n_qubit = qubit[0]
    
    # |00> GREATER VALUE == LEFTMOST
    #  ^

    prev_states_count = len(prev_states)

    # CHECK STATE COMPLEXITY
    if prev_states_count < num_states:
        # states increased, create FORK
        # assumes HAD gate order is qubit 0 --> qubit MAX
        for i in range(0, num_states // 2):
            # create edge to itself
            fork_self = {
                "start": (layer, i),
                "end": (layer + 1, i),
                "amplitude": new_layer["amplitudes"][i],
                "phase": new_layer["phases"][i],
                "old_phase": old_layer["phases"][i]
            }
            # create the paired edge
            fork_pair = {
                "start": (layer, i),
                "end": (layer + 1, i + num_states // 2),
                "amplitude": new_layer["amplitudes"][i],
                "phase": new_layer["phases"][i],
                "old_phase": old_layer["phases"][i]
            }

            edges.append(fork_self)
            edges.append(fork_pair)

    else:
        # calculate stride based on the qubit manipulated (MSB = 0, LSB = n-1)
        stride = 2 ** (n_qubit)
        #print("The stride is now", stride)
        
        for i in reversed(prev_states):
            # calculate the target state index based on stride
            target_state = i ^ stride  # XOR to find the "target" in the superposition

            # Combine amplitudes and phases from both source states
            contribution = (
                old_layer["amplitudes"][i] * np.exp(1j * old_layer["phases"][i]) +
                old_layer["amplitudes"][target_state] * np.exp(1j * old_layer["phases"][target_state])
            )
            # If the contribution is non-zero, create an edge
            if abs(contribution) > 1e-10:  # Account for floating-point precision
                join_edge = {
                    "start": (layer, i),
                    "end": (layer + 1, target_state),
                    "amplitude": abs(contribution),
                    "phase": np.angle(contribution),  # Keep resulting phase
                    "old_phase": old_layer["phases"][i]
                }
            else:
                join_edge = {
                    "start": (layer, i),
                    "end": (layer + 1, target_state),
                    "amplitude": old_layer["amplitudes"][target_state],
                    "phase": old_layer["phases"][target_state],
                    "old_phase": old_layer["phases"][target_state]
                }
            edges.append(join_edge)
    return edges