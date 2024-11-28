from qiskit import QuantumCircuit
import numpy as np

def generate_qpe():
    # number of qubits: 3 for the phase register, 1 for the eigenstate
    n_phase_qubits = 3
    eigen_qubits = 1

    qc = QuantumCircuit(n_phase_qubits + eigen_qubits, n_phase_qubits)

    # prepare the eigenstate |1⟩
    qc.x(n_phase_qubits)  # Apply an X gate to the eigenstate qubit

    # apply HAD to the phase register
    for i in range(n_phase_qubits):
        qc.h(i)

    repetitions = 1
    for qubit in range(n_phase_qubits):
        for i in range(repetitions):
            qc.cp(np.pi/4, qubit, 3); # the controlled phase rotation
        repetitions *= 2

    # controlled unitary operations (controlled rotations)
    #for q in range(n_phase_qubits):
    #    angle = np.pi / 4**(q + 1)  # Rotation angle for the controlled-U
    #    qc.cp(angle, q, n_phase_qubits)  # Controlled phase rotation

    qft_dagger(qc, n_phase_qubits)

    # Step 4: Inverse QFT (IQFT) on the phase register
    # Reverse qubits order using swap
    #for i in range(n_phase_qubits // 2):
    #    qc.swap(i, n_phase_qubits - i - 1)

    # Apply controlled rotations and Hadamard gates
    #for q in range(n_phase_qubits):
    #    for j in range(q):
    #        qc.cp(-np.pi / 2**(q - j), j, q)  # Controlled-phase gates
    #    qc.h(q)

    # Step 5: Measure the phase register
    #qc.measure(range(n_phase_qubits), range(n_phase_qubits))

    return qc

def qft_dagger(qc, n):
    """n-qubit QFTdagger the first n qubits in circ"""
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)