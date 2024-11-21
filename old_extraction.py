from gates.newhad import HAD_NEW
from gates.pauli_x import NOT
from gates.crot import CROT
from gates.swap import SWAP

from visualization.circle_notation import QubitSystem

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
qc.x(1)

qc.h(2) # HAD on most significant qubit
qc.cp(np.pi/2, 1, 2) # CROT qubit 1 to qubit 2, distance 1
qc.cp(np.pi/4, 0, 2) # CROT qubit 2 to qubit 0, distance 2
# Second block
qc.h(1) # HAD on second most significant qubit
qc.cp(np.pi/2, 0, 1) # CROT qubit 0 to qubit 1, distance 1
# Last block
qc.h(0) # HAD on least significant qubit
qc.swap(0,2) # SWAP qubit 0 and qubit 2

# Initialize the state vector
state = Statevector.from_int(0, dims=2**qc.num_qubits)  # Initial state |00>

# Initialize visualization data
visualization_data = {"layers": [], "edges": [], "gates": []}

# Starting layer (single vertex for |0>)
visualization_data["layers"].append({
    "layer": 0,
    "amplitudes": [1.0],            # Single amplitude for the initial state
    "phases": [0.0],              # No phase at the beginning
})

# Track mapping of current states (index in statevector) to layer vertices
previous_states = [0]   # previous state is prepped as 0
old_layer = {"layer": 0, "amplitudes": [1.0], "phases": [0.0]}

new_prev_state = state.data
print("begining state:", new_prev_state)

# evolve the state step-by-step
for layer, instruction in enumerate(qc.data):
    # extract the operation (gate)
    gate = instruction.operation
    print("Step Layer", layer, "gate", gate.name)
    # add gate name to list
    visualization_data["gates"].append(gate.name)

    # get target qubits
    qubits = [q._index for q in instruction.qubits]
    # evolve the state
    state = state.evolve(gate, qargs=qubits)
    print("new state:", state.data)

    # extract amplitudes and phases
    amplitudes = np.abs(state.data)
    phases = np.angle(state.data)
    
    # determine non-zero states
    non_zero_indices = [i for i, amp in enumerate(amplitudes) if amp > 1e-6]
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
        new_edges = HAD_NEW(qubits, new_prev_state, layer, state.data, phases)
    if (gate.name == "x"):
        print("Applying NOT Gate")
        new_edges = NOT(qubits, previous_states, layer, amplitudes, phases, old_layer)
    if (gate.name == "cp"):
        print("Applying CROT Gate")
        new_edges = CROT(previous_states, layer, amplitudes, phases, old_layer)
    if (gate.name == "swap"):
        new_edges = SWAP(qubits, previous_states, layer, amplitudes, phases, old_layer)

    visualization_data["layers"].append(new_layer)

    for edge in new_edges:
        visualization_data["edges"].append(edge)

    # Keep track of previous case or edge logic
    # placing the edge at correct index when JOIN
    previous_states = non_zero_indices
    old_layer = new_layer
    new_prev_state = state.data
    print()

# Save to a file
with open('visualization_data.json', 'w') as f:
    json.dump(visualization_data, f)

statevector = Statevector(state)
#visualize(statevector.data)