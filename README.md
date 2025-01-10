# DD2375 Project: Visualizing Quantum Parallelism
This is the github repository for the Quantum Computing project part of the course DD2375. This project aims to automatically visualize and measure the quantum parallelism part of quantum algorithms. The following section contains information on the repo structure as well as how to run and visualize your own circuits.

# Installation
To install a fresh version, you can create a virtual environment:
## Installation Linux/Mac
```bash
python3 -m venv venv  
source venv/bin/activate
```

## Installation Windows
```bash
python -m venv venv  
source venv/scripts/activate
```

For installing all the dependencies of the project: 

```bash
pip install -r requirements.txt
```

## Launch Existing Environment:
To launch an already created virtual environment (with all dependencies installed) you can just run the following command:
```bash
source venv/scripts/activate
```

# Running Visualizer
## Visualize
To run the visualizer, use the command:
```bash
python main_script.py
```
This will launch the application. First, it will run the main loop, extracting data from each unitary operation in the circuit. Secondly it will calculate the quantum parallelism. Thirdly, and often the most time-consuming part, it will open a new HTML window to start rendering the graph.

By default, a 4-qubit system of a grover iteration will be visualized. **Please see the [Adding Circuit](link)** below for instructions on how to visualize your own circuits.

# Repository
 * [circuits](./circuits)
   * [circuit.py](./circuits/circuit.py)
   * ...
 * [extraction](./extraction)
   * [gates](./extraction/gates)
        * ...
   * [extract_quantum_data.py](./extraction/extract_quantum_data.py)
 * [visualization](./visualization)
 * [main_script.py](./main_script.py)
 * [README.md](./README.md)

## [Adding your own Circuit ](#link)
The [circuits](./circuits) directory contains the [```circuit.py```](./circuits/circuit.py) script where the user creates their circuit to visualize. Other scripts can be created in the same directory to keep circuits separated and structured, but they must be imported into the circuit script.

## Saving data as JSON
The [main_script.py](./main_script.py) has commented code for saving the visualization data as a JSON on row 37. This could be usefull if you dont want generate new data and reuse old. To use the function of saving/loading data you can uncomment the JSON section and comment/remove the ```extract_quantum_data``` function. Then you can use the ```load_visualization_data``` function to load your saved data.

**NOTE:** The visualization can become laggy when using too many qubits. You can test for yourself but I personally recommend to keep it below 6 to 7 qubits.

## Adding new Gates / Edge logic
If you would like to add new gates that are not captured by the existing gate logics, you can add your own edge creation logic in the [gates](./extraction/gates) directory. You can view the already existing gates to get an idea of how to implement the logic.

If you add a subcircuit and want to represent it as a single gate operation, like for instance an ORACLE that rotates a single state, you can name the subcircuit and then add a clause to the if-statements for edge logic in the [```extract_quantum_data.py```](./extraction/extract_quantum_data.py) script. **An example** of naming a subcircuit correctly can be seen in the [```grover_circuit.py```](./circuits/grover_circuit.py) script.

## Future Possible Expansions/Issues
* Implement edge logic for more gates (especially all the common ones).
* For plotly, fix responsiveness of graphs to better scale with different screen sizes.
* Try different 3D library instead of plotly to possibly improve performance, making it feasible to visualize circuits with a greater number of qubits.
* Improve edge logic to feature a single oracle / one script that can correctly identify the operation done and how edges should be created from said operation. Essentially make edge logic generic instead of dependent on clauses.
