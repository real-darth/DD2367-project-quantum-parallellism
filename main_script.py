import numpy as np
import json
from visualization.quantum_visualizer import visualize_quantum_parallelism
from visualization.ui_elements import add_ui_elements
from visualization.utils import extract_gate_labels
from extraction.extract_quantum_data import extract_quantum_data
from circuits.example_circuit import build_example_circuit

# load json data
def load_visualization_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# main function
if __name__ == "__main__":
    # build circuit
    qc = build_example_circuit()

    # extract visualization data
    data = extract_quantum_data(qc)

    #if True:
    #    exit()

    # save data to JSON
    #with open("visualization_data.json", "w") as f:
    #    json.dump(data, f)

    # load json
    #data = load_visualization_data('visualization_data.json')

    # generate computational basis states for UI
    num_states = max(len(layer['amplitudes']) for layer in data['layers'])
    computational_basis = [f"|{bin(i)[2:].zfill(int(np.log2(num_states)))}⟩" for i in range(num_states)]

    # create visualization
    fig = visualize_quantum_parallelism(data, computational_basis)

    # get gate name data
    gate_labels = extract_gate_labels(data)

    # add UI elements
    fig = add_ui_elements(fig, computational_basis, gate_labels, show_hierarchy=False)

    # save and display
    fig.write_html("quantum_plot.html", auto_open=True)
