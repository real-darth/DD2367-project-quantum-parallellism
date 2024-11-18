from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Define a simple quantum circuit
qc = QuantumCircuit(2)
qc.h(0)  # Apply Hadamard to qubit 0
qc.h(1)  # Apply Hadamard to qubit 1

# Initialize the state vector
state = Statevector.from_int(0, dims=2**qc.num_qubits)  # Initial state |00>

# List to store intermediate states
intermediate_states = []
intermediate_gates = []

# Evolve the state step-by-step
for instruction in qc.data:
    gate = instruction.operation  # Extract the operation (gate)
    qubits = [q._index for q in instruction.qubits]  # Get target qubits
    state = state.evolve(gate, qargs=qubits)  # Evolve the state
    intermediate_states.append(state)  # Store the state
    intermediate_gates.append(gate)

# Display intermediate states and quantum parallelism
for i, state in enumerate(intermediate_states):
    amplitudes = state.data
    parallel_states = sum(abs(a) > 1e-6 for a in amplitudes)  # Non-zero amplitudes
    print(f"Step {i + 1}: State = {state}")
    print(f"Step {i + 1}: {intermediate_gates[i].name}")
    print(f"Parallelism = {parallel_states}\n")


"""

# Convert the circuit to a DAG
dag = circuit_to_dag(qc)

print(dag)

# Print DAG nodes and edges
for node in dag.topological_op_nodes():  # Only iterate over operation nodes
    print(f"Node: {node.op.name}, Qubits: {[qubit._index for qubit in node.qargs]}")



# Create a graph from the DAG
G = nx.DiGraph()

# Add nodes and edges
for node in dag.topological_nodes():
    G.add_node(str(node), label=node.name)
    for succ in dag.successors(node):
        G.add_edge(str(node), str(succ))

# Plot the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000)
labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels=labels)
plt.show()

"""