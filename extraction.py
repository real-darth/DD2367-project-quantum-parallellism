from gates.hadamard import HAD

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
import json

# Define a simple quantum circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
qc.h(2)
qc.h(0)
qc.h(1)
qc.h(2)

# Initialize the state vector
state = Statevector.from_int(0, dims=2**qc.num_qubits)  # Initial state |00>


# Initialize visualization data
visualization_data = {"layers": [], "edges": []}

# Starting layer (single vertex for |0>)
visualization_data["layers"].append({
    "layer": 0,
    "amplitudes": [1.0],  # Single amplitude for the initial state
    "phases": [0.0]  # No phase at the beginning
})

# Track mapping of current states (index in statevector) to layer vertices
previous_layer_mapping = {0: 0}  # Maps state index -> vertex index in layer 0
previous_states = []

# Evolve the state step-by-step
for layer, instruction in enumerate(qc.data):
    print("Step Layer", layer)

    gate = instruction.operation  # Extract the operation (gate)
    qubits = [q._index for q in instruction.qubits]  # Get target qubits
    state = state.evolve(gate, qargs=qubits)  # Evolve the state
    
    # Extract amplitudes and phases
    amplitudes = np.abs(state.data)
    phases = np.angle(state.data)

    print("new state:", state)
    
    # Determine non-zero states (quantum parallelism)
    non_zero_indices = [i for i, amp in enumerate(amplitudes) if amp > 1e-6]
    print("non zero indices:", non_zero_indices)
    num_states = len(non_zero_indices)

    cleaned_amplitudes = [i for i, amp in enumerate(amplitudes)]

    # Add a new layer with only non-zero states
    new_layer_mapping = {}
    new_layer = {"layer": layer + 1, "amplitudes": [], "phases": []}
    
    for vertex_idx, state_idx in enumerate(cleaned_amplitudes):
        new_layer["amplitudes"].append(amplitudes[state_idx])
        new_layer["phases"].append(phases[state_idx])
        new_layer_mapping[state_idx] = vertex_idx
    
    visualization_data["layers"].append(new_layer)
    

    # EDGE LOGIC
    if (gate.name == "h"):
        print("Applying HAD Gate")
        new_edges = HAD(qubits, previous_states, num_states, layer)


    for edge in new_edges:
        visualization_data["edges"].append(edge)

    # Update mapping for the next iteration
    previous_layer_mapping = new_layer_mapping
    # Keep track of previous case or edge logic
    # placing the edge at correct index when JOIN
    previous_states = non_zero_indices
    print()


# Save or return the visualization data
#print(json.dumps(visualization_data, indent=4))

# Save to a file
with open('visualization_data.json', 'w') as f:
    json.dump(visualization_data, f)
