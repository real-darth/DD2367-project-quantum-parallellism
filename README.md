# DD2375 Project: Visualizing Quantum Parallellism
This is the github repository for the Quantum Computing project part of the course DD2375. This project aims to automatically visualize and measure the quantum parallelism part of quantum algorithms. The following section contains information on the repo structure as well as how to run and visualize your own circuits.

# Installation
## Installation Windows
To install a fresh version on windows, you can create a virtual environment:
```bash
python -m venv venv  
source venv/scripts/activate
```
For installing all the dependecies of the project: 

```bash
pip install -r requirements.txt
```

## Launch Windows
To launch a already created virtual enviornment (with all dependencies installed) you can just run the following command:
```bash
source venv/scripts/activate
```

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

## Running
To run the visualizer, use the command:
```bash
python main_script.py
```
This will launch the application. First it will run the main loop extracting data from each unitary operation part of the circuit. Secondly it will calculate the quantum parallelism. Thirdly and often the most time consuming part, it will open a new HTML window and start rendering the graph.

## Adding your own Circuit
The [circuits](./circuits) directory contain the [```circuit.py```](./circuits/circuit.py) script where the user creates thier circuit to visualize. Other scripts can be created in the same directory to keep circuits seperated and structured, but they have to be imported to the circuit script.

**NOTE:** The visualization can become laggy when using too many qubits. You can test for yourself but I personally recommend to keep it below 6 to 7 qubits.

## Adding new Gates / Edge logic
If you would like to add new gates that are not captured by the existing gate logics, you can add your own edge creation logic in the [gates](./extraction/gates) directory. You can view the already existing gates to get an idea of how to implement the logic.

If you add a subcircuit and want to represent it as a single gate operation, like for instance an ORACLE that rotates a single state, you can name the subcircuit and then add a clause to the if-statements for edge logic in the [```extract_quantum_data.py```](./extraction/extract_quantum_data.py) script. **An example** of naming a subcircuit correctly can be seen in the [```grover_circuit.py```](./circuits/grover_circuit.py) script.

## Future Possible Expansions
* Try different library from plotly to possibly improve performance. Making it possible to visualize circuits with greater number of qubits.
* For plotly, fix responsiveness of graphs to better scale with different screen sizes.
* Improve edge logic to feature a single oracle / one script that can correctly identify the operation done and how edges should be created from said operation. Essentially make edge logic generic instead of dependent on clauses.