from qiskit import QuantumCircuit
from .utils import MCZ

def generate_circuit(n):
    # generate circuit withb n qubits
    qc = QuantumCircuit(n)
    # apply Hadamard gate to each qubit, uniform superposition
    for i in range(n):
        qc.h(i)
    return qc

def diffuse(qc, n):
    # apply HAD gate to all qubits
    for i in range(n):
        qc.h(i)

    for i in range(n):
        qc.x(i)

    # apply multi-controlled Z
    controls = list(range(1, n))
    MCZ(qc, controls, 0)

    for i in range(n):
        qc.x(i)

    # apply Hadamard again to all qubits
    for i in range(n):
        qc.h(i)

def oracle_for_target_state(qc):
    qubits = qc.num_qubits # get amount of qubits form circuit
    sub_circuit = QuantumCircuit(qubits, name="Oracle")
    # flip qubits to match |0011⟩ (X on q3 and q2 to target the '0' states)
    sub_circuit.x(3)
    sub_circuit.x(2)

    # apply multi-controlled Z
    controls = list(range(1, qubits))
    MCZ(qc, controls, 0)

    # undo the X gates
    sub_circuit.x(3)
    sub_circuit.x(2)
    
    oracle_gate = sub_circuit.to_instruction(label="Oracle")
    qc.append(oracle_gate, list(range(qubits)))

def grover_iteration(n, iterations):
    qc = generate_circuit(n)
    for _ in range(iterations):
        oracle_for_target_state(qc)
        diffuse(qc, n)

    return qc
