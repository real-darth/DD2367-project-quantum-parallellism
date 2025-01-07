from visualization.circle_notation import QubitSystem

def visualize(vector, n = 3):
    "Circle notation visualization of a quantum state vector"
    # initialize with n qubits
    qubit_system = QubitSystem(n_qubits=n)

    # set the state vector
    qubit_system.qubit = vector

    # visualize the state
    qubit_system.viz2()

def create_start(visualization_data):
    "Create the start layer for the visualization data"
    # starting layer (single vertex for |0>)
    visualization_data["layers"].append({
        "layer": 0,
        "amplitudes": [1.0],
        "phases": [0.0],
    })

    # second layer for applying the first gate
    visualization_data["layers"].append({
        "layer": 1,
        "amplitudes": [1.0],
        "phases": [0.0],
    })

    # edge between the two new layers
    edge = {
        "start": (0, 0),
        "end": (1, 0),
        "amplitude": 1,
        "phase": 0,
        "old_phase": 0
    }

    visualization_data["edges"].append(edge)
    visualization_data["gates"].append("Start")