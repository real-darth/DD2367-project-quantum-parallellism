from qiskit import QuantumCircuit
import numpy as np

def build_example_circuit():
    #qc = myQFT()
    
    # create a 3-qubit circuit (for 8 possible rooms/states)
    n = 4
    iterations = 1
    # run grover iteration
    qc = grover_iteration(n, iterations)
    return qc

def myQFT():
    qc = QuantumCircuit(3)
    qc.x(1)

    qc.h(2)  # HAD on most significant qubit
    qc.cp(np.pi/2, 1, 2)  # CROT qubit 1 to qubit 2, distance 1
    qc.cp(np.pi/4, 0, 2)  # CROT qubit 2 to qubit 0, distance 2
    # Second block
    qc.h(1)  # HAD on second most significant qubit
    qc.cp(np.pi/2, 0, 1)  # CROT qubit 0 to qubit 1, distance 1
    # Last block
    qc.h(0)  # HAD on least significant qubit
    qc.swap(0, 2)  # SWAP qubit 0 and qubit 2
    
    return qc

def generate_circuit(n):
    # generate circuit withb n qubits
    qc = QuantumCircuit(n)
    # apply Hadamard gate to each qubit, uniform superposition
    for i in range(n):
        qc.h(i)
    return qc

def oracle_for_target_state(qc):
    sub_circuit = QuantumCircuit(4, name="Oracle")
    # Flip qubits to match |0011⟩ (X on q3 and q2 to target the '0' states)
    sub_circuit.x(3)
    sub_circuit.x(2)

    # Apply multi-controlled Z
    sub_circuit.h(0)         # Convert Z on |0> to an X-equivalent
    sub_circuit.mcx([3, 2, 1], 0)  # Multi-controlled X (3 controls)
    sub_circuit.h(0)         # Convert back to Z

    # Undo the X gates
    sub_circuit.x(3)
    sub_circuit.x(2)

    oracle_gate = sub_circuit.to_instruction(label="Oracle")

    qc.append(oracle_gate, [0, 1, 2, 3])

def diffuse(qc, n):
    # apply HAD gate to all qubits
    for i in range(n):
        qc.h(i)

    for i in range(n):
        qc.x(i)

    qc.ccz(0, 1, 2)

    for i in range(n):
        qc.x(i)

    # apply Hadamard again to all qubits
    for i in range(n):
        qc.h(i)

def grover_iteration(n, iterations):
    qc = generate_circuit(n)
    for _ in range(iterations):
        oracle_for_target_state(qc)
        diffuse(qc, n)

    return qc