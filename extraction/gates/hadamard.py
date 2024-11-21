import numpy as np

def HAD(qubit, prev_state, layer, new_state, phases, threshold=1e-10):
    edges = []
    target_qubit = qubit[0]

    # Apply the Hadamard gate to the target qubit
    for i in range(len(prev_state)):
        # Calculate the target states after applying H
        target_zero = i  # Target for |0>
        target_one = i ^ (1 << target_qubit)  # Target for |1> (bit flip on target qubit)
        
        if np.abs(prev_state[i]) > threshold:
            print(f"State {i}: Amplitude {prev_state[i]} -> Targets {target_zero}, {target_one}")

        if np.abs(prev_state[i]) > threshold:  # Check if the previous state is significant
            # Amplitudes for the resulting states
            amp_zero = prev_state[i] / np.sqrt(2)
            amp_one = prev_state[i] / np.sqrt(2)

            # Cross-check new state amplitudes
            if np.abs(new_state[target_zero]) > threshold:
                edges.append({
                    "start": (layer, i),
                    "end": (layer + 1, target_zero),
                    "amplitude": np.abs(amp_zero),
                    "phase": phases[target_zero],
                    "old_phase": np.angle(amp_zero)
                })
            if np.abs(new_state[target_one]) > threshold:
                edges.append({
                    "start": (layer, i),
                    "end": (layer + 1, target_one),
                    "amplitude": np.abs(amp_one),
                    "phase": phases[target_one],
                    "old_phase": np.angle(amp_one)
                })
    
    return edges
