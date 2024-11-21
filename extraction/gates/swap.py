import numpy as np

def SWAP(qubits, prev_state, layer, amplitudes, phases, old_layer, threshold=1e-10):
    edges = []
    # The two qubits being swapped
    q1 = qubits[0]
    q2 = qubits[1]
    
    # Apply the SWAP gate
    for i in range(0, len(prev_state)):
        # Determine which qubits are swapped
        bit1 = (i >> q1) & 1  # Extract the bit at position q1
        bit2 = (i >> q2) & 1  # Extract the bit at position q2
        
        # Swap the bits to determine the new index
        swapped_index = i ^ ((bit1 ^ bit2) << q1) ^ ((bit1 ^ bit2) << q2)
        
        if amplitudes[i] > threshold:
            print(f"State {i}: Amplitude {prev_state[i]} -> Swapped State {swapped_index}")
        
        if amplitudes[i] > threshold:  # Check if the previous state is significant
            # Preserve the amplitude (SWAP does not change amplitudes or phases)
            amplitude = amplitudes[i]
            phase = phases[swapped_index]

            # Add an edge for visualization
            edges.append({
                "start": (layer, i),
                "end": (layer + 1, swapped_index),
                "amplitude": amplitude,
                "phase": phase,
                "old_phase": old_layer["phases"][i]
            })
    
    return edges