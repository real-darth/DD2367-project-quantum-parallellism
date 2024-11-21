from qiskit import QuantumCircuit
import numpy as np

def build_example_circuit():
    # Number of qubits
    n_qubits = 4
    qc = QuantumCircuit(n_qubits)

    # Apply Hadamards to create uniform superposition
    qc.h(range(n_qubits))

    # Apply phase shifts
    for k in range(n_qubits):
        phase = (2 * np.pi * 2) / (2**n_qubits)  # Encode |2>
        for j in range(2**k):
            qc.p(phase * j, k)


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