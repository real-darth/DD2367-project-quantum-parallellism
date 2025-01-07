#source: https://github.com/qiskit-community/qiskit-textbook/blob/main/content/ch-algorithms/quantum-phase-estimation.ipynb

from qiskit import QuantumCircuit
import numpy as np

def generate_qpe():
    "Generates a Quantum Phase Estimation (QPE) circuit for T-gate phase estimation"
    # number of qubits: 3 for the phase register, 1 for the eigenstate
    n_phase_qubits = 3
    eigen_qubits = 1

    qc = QuantumCircuit(n_phase_qubits + eigen_qubits, n_phase_qubits)

    # prepare the eigenstate |1⟩
    qc.x(n_phase_qubits)  # X gate to the eigenstate qubit

    # apply HAD to the phase register
    for i in range(n_phase_qubits):
        qc.h(i)

    # controlled unitary operations (controlled rotations)
    repetitions = 1
    for qubit in range(n_phase_qubits):
        for i in range(repetitions):
            qc.cp(np.pi/4, qubit, 3); # the controlled phase rotation
        repetitions *= 2

    # inverse QFT (IQFT) on the phase register
    qft_dagger(qc, n_phase_qubits)

    return qc

def qft_dagger(qc, n):
    """n-qubit QFTdagger the first n qubits in circ"""
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2 ** (j-m)), m, j)
        qc.h(j)