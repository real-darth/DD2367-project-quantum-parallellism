from gates.hadamard import HAD
from gates.pauli_x import NOT
from gates.crot import CROT

from circle_notation import QubitSystem

def visualize(vector, n = 3):
    # initialize with n qubits
    qubit_system = QubitSystem(n_qubits=n)

    # set the state vector
    qubit_system.qubit = vector

    # visualize the state
    qubit_system.viz2()

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
import json

# Define a simple quantum circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
qc.h(2)
qc.cp(np.pi/2, 1, 2)
qc.cp(np.pi/4, 0, 2)
qc.x(2)
qc.h(2)

#qc.x(1)
#qc.x(2)

# Initialize the state vector
state = Statevector.from_int(0, dims=2**qc.num_qubits)  # Initial state |00>

# Initialize visualization data
visualization_data = {"layers": [], "edges": []}

# Starting layer (single vertex for |0>)
visualization_data["layers"].append({
    "layer": 0,
    "amplitudes": [1.0],            # Single amplitude for the initial state
    "phases": [0.0],              # No phase at the beginning
})

# Track mapping of current states (index in statevector) to layer vertices
previous_states = []
old_layer = {"layer": 0, "amplitudes": [1.0], "phases": [0.0]}

# Evolve the state step-by-step
for layer, instruction in enumerate(qc.data):
    gate = instruction.operation  # Extract the operation (gate)
    print("Step Layer", layer, "gate", gate.name)

    # get target qubits
    qubits = [q._index for q in instruction.qubits]
    # evolve the state
    state = state.evolve(gate, qargs=qubits)
    #print("new state:", state)

    # extract amplitudes and phases
    amplitudes = np.abs(state.data)
    phases = np.angle(state.data)
    print("phases:", phases)
    
    # determine non-zero states
    non_zero_indices = [i for i, amp in enumerate(amplitudes) if amp > 1e-6]
    #print("non zero indices:", non_zero_indices)
    num_states = len(non_zero_indices)

    # add a new layer with only non-zero states
    new_layer = {"layer": layer + 1, "amplitudes": [], "phases": []}
    
    # VERTEX LOGIC
    for state_idx in range(0, len(amplitudes)):
        new_layer["amplitudes"].append(amplitudes[state_idx])
        new_layer["phases"].append(phases[state_idx])

    # EDGE LOGIC
    if (gate.name == "h"):
        print("Applying HAD Gate")
        new_edges = HAD(qubits, previous_states, num_states, layer, new_layer, old_layer)
    if (gate.name == "x"):
        print("Applying NOT Gate")
        new_edges = NOT(qubits, previous_states, layer, amplitudes, phases, old_layer)
    if (gate.name == "cp"):
        print("Applying CROT Gate")
        new_edges = CROT(qubits, previous_states, layer, amplitudes, phases, old_layer)

    visualization_data["layers"].append(new_layer)

    for edge in new_edges:
        visualization_data["edges"].append(edge)

    # Keep track of previous case or edge logic
    # placing the edge at correct index when JOIN
    previous_states = non_zero_indices
    old_layer = new_layer
    print()

statevector = Statevector(state)
#visualize(statevector.data)

# Save to a file
with open('visualization_data.json', 'w') as f:
    json.dump(visualization_data, f)
