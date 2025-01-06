import numpy as np
from qiskit.quantum_info import Statevector

from .gates.hadamard import HAD
from .gates.pauli_x import NOT
from .gates.rotation import ROTATE
from .gates.swap import SWAP
from .utils import create_start, visualize
from visualization.utils import VISUALIZATION_THRESHOLD

# offset the visualization for including a START point
OFFSET = 1
ROTATION_GATE_NAMES = ["z", "cp", "cz", "ccz", "MCZ", "Oracle"]

def extract_quantum_data(qc, visualize_quantum_vector=False):
    """Extract quantum circuit data into a dictionary."""
    # initialize state vector
    state = Statevector.from_int(0, dims=2**qc.num_qubits)
    # create dictionary for data
    # layers represent the gate-layer, edges represent the threads and gates represents the gate names
    visualization_data = {"layers": [], "edges": [], "gates": []}
    # create starting state for visualization
    create_start(visualization_data)

    # track the previous states
    previous_indexed_state = [0]
    old_layer = {"layer": 1, "amplitudes": [1.0], "phases": [0.0, 0.0]}
    previous_state_data = state.data

    # process each instruction in the circuit step by step
    for layer_index, instruction in enumerate(qc.data):
        layer_index += OFFSET

        gate = instruction.operation
        print("Running on gate", gate.name)

        # evolve the state
        qubits = [q._index for q in instruction.qubits]
        state = state.evolve(gate, qargs=qubits)

        # calculate the new states amplitudes and phases
        amplitudes = np.abs(state.data)
        phases = np.angle(state.data)

        #print("State amplitude", amplitudes)
        #print("State phase", phases)

        # ---------------------------- VERTEX -------------------------------
        # add new layer with amplitudes and phases vertex points
        new_layer = {
            "layer": layer_index,
            "amplitudes": amplitudes.tolist(),
            "phases": phases.tolist(),
        }
        # ---------------------------- VERTEX -------------------------------

        # ---------------------------- GATES --------------------------------
        # gate-specific edge logic
        if gate.name == "h":
            new_edges = HAD(qubits, previous_state_data, layer_index, state.data, amplitudes, phases, VISUALIZATION_THRESHOLD)
        elif gate.name == "x":
            new_edges = NOT(qubits, previous_indexed_state, layer_index, amplitudes, phases, old_layer)
        elif gate.name == "swap":
            new_edges = SWAP(qubits, previous_state_data, layer_index, amplitudes, phases, old_layer, VISUALIZATION_THRESHOLD)
        # any rotation on phases are visualized with the ROTATE function
        elif gate.name in ROTATION_GATE_NAMES:
            new_edges = ROTATE(previous_indexed_state, layer_index, amplitudes, phases, old_layer)
        # ---------------------------- GATES --------------------------------

        # add vertecies, edges and gate label to data
        visualization_data["layers"].append(new_layer)
        visualization_data["edges"].extend(new_edges)
        visualization_data["gates"].append(gate.name)

        # prepare next iteration
        previous_indexed_state = [i for i, amp in enumerate(amplitudes) if amp > VISUALIZATION_THRESHOLD]
        old_layer = new_layer
        previous_state_data = state.data

    # OPTIONAL: cirlce notation viusalizer 
    if (visualize_quantum_vector == True):
        statevector = Statevector(state)
        visualize(statevector.data, qc.num_qubits)

    return visualization_data
