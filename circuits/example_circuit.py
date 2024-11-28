from qiskit import QuantumCircuit
import numpy as np

from .grover_circuit import grover_iteration
from .qpe_circuit import generate_qpe

def build_example_circuit():
    qc = generate_qpe()
    return qc

def inteference_test():
    qc = QuantumCircuit(2)
    # Apply a Hadamard gate to both qubits
    qc.h(0)
    qc.h(1)

    # Add a CZ (controlled-Z) gate to introduce phase interaction
    qc.cz(0, 1)

    # Apply another Hadamard gate to both qubits to test interference
    qc.h(0)
    qc.h(1)
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
