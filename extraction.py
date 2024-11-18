from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
import json

# Define a simple quantum circuit
qc = QuantumCircuit(2)
qc.h(0)  # Apply Hadamard to qubit 0
qc.h(1)  # Apply Hadamard to qubit 1

# Initialize the state vector
state = Statevector.from_int(0, dims=2**qc.num_qubits)  # Initial state |00>

# List to store intermediate states and visualization data
intermediate_states = []
visualization_data = {"layers": [], "edges": []}

# Evolve the state step-by-step
for layer, instruction in enumerate(qc.data):
    gate = instruction.operation  # Extract the operation (gate)
    qubits = [q._index for q in instruction.qubits]  # Get target qubits
    state = state.evolve(gate, qargs=qubits)  # Evolve the state
    amplitudes = np.abs(state.data)
    phases = np.angle(state.data)

    # Add layer data
    visualization_data["layers"].append({
        "layer": layer,
        "amplitudes": amplitudes.tolist(),
        "phases": phases.tolist()
    })

    # Add edges
    for qubit, (amplitude, phase) in enumerate(zip(amplitudes, phases)):
        if amplitude > 1e-6:  # Ignore negligible states
            visualization_data["edges"].append({
                "start": (layer - 1, qubit),
                "end": (layer, qubit),
                "amplitude": amplitude,
                "phase": phase
            })

# Save or return the visualization data
print(visualization_data)

# Save visualization_data to a file
with open('visualization_data.json', 'w') as f:
    json.dump(visualization_data, f)
