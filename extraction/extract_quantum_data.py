import numpy as np
from qiskit.quantum_info import Statevector

from .gates.hadamard import HAD
from .gates.pauli_x import NOT
from .gates.crot import CROT
from .gates.swap import SWAP
from .gates.control_control_z import CCZ

from visualization.circle_notation import QubitSystem

def visualize(vector, n = 3):
    # initialize with n qubits
    qubit_system = QubitSystem(n_qubits=n)

    # set the state vector
    qubit_system.qubit = vector

    # visualize the state
    qubit_system.viz2()

def extract_quantum_data(qc):
    """Extract quantum circuit data into a JSON-compatible dictionary."""
    # Initialize state vector
    state = Statevector.from_int(0, dims=2**qc.num_qubits)

    visualization_data = {"layers": [], "edges": [], "gates": []}

    # Starting layer (single vertex for |0>)
    visualization_data["layers"].append({
        "layer": 0,
        "amplitudes": [1.0],
        "phases": [0.0],
    })

    # Track the previous states
    previous_states = [0]
    old_layer = {"layer": 0, "amplitudes": [1.0], "phases": [0.0]}
    new_prev_state = state.data

    # Process each instruction in the circuit
    for layer, instruction in enumerate(qc.data):
        gate = instruction.operation
        print("Running on gate", gate.name)
        visualization_data["gates"].append(gate.name)

        qubits = [q._index for q in instruction.qubits]
        state = state.evolve(gate, qargs=qubits)

        amplitudes = np.abs(state.data)
        phases = np.angle(state.data)

        # Add new layer with non-zero states
        new_layer = {
            "layer": layer + 1,
            "amplitudes": amplitudes.tolist(),
            "phases": phases.tolist(),
        }

        # Gate-specific edge logic
        if gate.name == "h":
            new_edges = HAD(qubits, new_prev_state, layer, state.data, phases)
        elif gate.name == "x":
            new_edges = NOT(qubits, previous_states, layer, amplitudes, phases, old_layer)
        elif gate.name == "cp":
            new_edges = CROT(previous_states, layer, amplitudes, phases, old_layer)
        elif gate.name == "swap":
            new_edges = SWAP(qubits, previous_states, layer, amplitudes, phases, old_layer)
        elif gate.name == "ccz":
            new_edges = CCZ(qubits, previous_states, layer, state.data, amplitudes, phases)

        visualization_data["layers"].append(new_layer)
        visualization_data["edges"].extend(new_edges)

        previous_states = [i for i, amp in enumerate(amplitudes) if amp > 1e-6]
        old_layer = new_layer
        new_prev_state = state.data

        print("Amplitdues", amplitudes)

    statevector = Statevector(state)
    visualize(statevector.data, qc.num_qubits)

    return visualization_data
