import numpy as np
import json
from circuits.example_circuit import build_example_circuit
from extraction.extract_quantum_data import extract_quantum_data
from extraction.measure_parallelism import calculate_tinfinity, calculate_tw
from visualization.quantum_visualizer import visualize_quantum_parallelism
from visualization.ui_elements import add_ui_elements
from visualization.utils import extract_gate_labels

# load json data
def load_visualization_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# main function
if __name__ == "__main__":
    # build circuit
    qc = build_example_circuit()

    # extract visualization data
    vs_data = extract_quantum_data(qc)

    # extract parallelism measurement
    tw = calculate_tw(vs_data)
    tinfinity = calculate_tinfinity(vs_data)

    print("Total Work (Tw):", tw)
    print("Critical Path Length (T_infinity):", tinfinity)

    # save data to JSON
    #with open("visualization_data.json", "w") as f:
    #    json.dump(vs_data, f)

    #if True:
    #    exit()

    # load json
    #data = load_visualization_data('visualization_data.json')

    # generate computational basis states for UI
    num_states = max(len(layer['amplitudes']) for layer in vs_data['layers'])
    computational_basis = [f"|{bin(i)[2:].zfill(int(np.log2(num_states)))}⟩" for i in range(num_states)]

    # create visualization
    fig = visualize_quantum_parallelism(vs_data, computational_basis)

    # get gate name from data
    gate_labels = extract_gate_labels(vs_data)

    # add UI elements
    fig = add_ui_elements(fig, computational_basis, gate_labels, show_hierarchy=False)

    # save and display
    fig.write_html("quantum_plot.html", auto_open=True)
