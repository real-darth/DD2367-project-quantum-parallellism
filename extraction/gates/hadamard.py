import numpy as np

def HAD(qubit, previous_state_data, layer, new_state, amplitudes, phases, threshold=1e-10):
    edges = []
    # extract target qubit from gate info
    target_qubit = qubit[0]

    # apply the Hadamard gate to the target qubit
    for i in range(len(previous_state_data)):
        # calculate the target states after applying H
        target_zero = i  # Target for |0>
        target_one = i ^ (1 << target_qubit)  # Target for |1> (bit flip on target qubit)
        
        #if np.abs(prev_state[i]) > threshold:
        #    print(f"State {i}: Amplitude {prev_state[i]} -> Targets {target_zero}, {target_one}")

        if np.abs(previous_state_data[i]) > threshold:  # check if the previous state is significant
            previous_phase = np.angle(previous_state_data[i])
            # cross-check new state amplitudes
            if np.abs(new_state[target_zero]) > threshold:
                edges.append({
                    "start": (layer, i),
                    "end": (layer + 1, target_zero),
                    "amplitude": amplitudes[target_zero],
                    "phase": phases[target_zero],
                    "old_phase": previous_phase
                })
            if np.abs(new_state[target_one]) > threshold:
                edges.append({
                    "start": (layer, i),
                    "end": (layer + 1, target_one),
                    "amplitude": amplitudes[target_one],
                    "phase": phases[target_one],
                    "old_phase": previous_phase
                })
    
    return edges
