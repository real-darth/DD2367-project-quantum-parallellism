import numpy as np

def SWAP(qubits, previous_state_index, layer, amplitudes, phases, old_layer, threshold=1e-10):
    """
    SWAP gate visualization, which swaps the states of two qubits based on the given qubits.

    Args:
        qubits (list): Indicating which qubits are manipulated (e.g., [q1, q2]).
        previous_state_index (list): Previous states indices.
        layer (int): Current layer index.
        amplitudes (list): Precomputed amplitudes for the evolved state.
        phases (list): Precomputed phases for the evolved state.
    """
    edges = []
    # extract the two qubits being swapped
    q1 = qubits[0]
    q2 = qubits[1]
    
    # apply the SWAP gate
    for i in previous_state_index:
        # determine which qubits are swapped
        bit1 = (i >> q1) & 1  # extract the bit at position q1
        bit2 = (i >> q2) & 1  # extract the bit at position q2
        
        # swap the bits to determine the new index
        swapped_index = i ^ ((bit1 ^ bit2) << q1) ^ ((bit1 ^ bit2) << q2)
        
        #if amplitudes[i] > threshold:
            #print(f"State {i}: Amplitude {prev_state[i]} -> Swapped State {swapped_index}")
        
        if amplitudes[i] > threshold:
            
            amplitude = amplitudes[swapped_index]
            phase = phases[swapped_index]

            # add edge
            edges.append({
                "start": (layer, i),
                "end": (layer + 1, swapped_index),
                "amplitude": amplitude,
                "phase": phase,
                "old_phase": old_layer["phases"][i]
            })
    
    return edges