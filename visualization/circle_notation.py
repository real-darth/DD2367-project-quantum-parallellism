import numpy as np
import matplotlib
from matplotlib import pyplot as plt, patches
import cmath, math
import random
import sys

class QubitSystem:
    # init_state = initial state
    # n_qubits = number of the qubits in the system
    def __init__(self, n_qubits=1,label='qs X'):
        self.n_qubits = n_qubits
        self.n_states = 2**n_qubits
        self.label = label
        
        print("Quantum System Allocated")
        print("Number of qubits = ", self.n_qubits)
        print("Number of possible states = ", self.n_states)
        
        # allocate qubit system as an array of complex numbers
        self.qubit = np.zeros((self.n_states),dtype=complex)
        self.ampli_qubit = np.zeros((self.n_states),dtype=float)
        self.phase_qubit = np.zeros((self.n_states),dtype=float)

    # Use Circle Notation
    def viz2(self):
        # Calculate amplitude and phase
        self.prob_qubit = np.absolute(self.qubit)
        self.phase_qubit = np.angle(self.qubit)
        
        # Determine number of rows and columns
        cols = 8  # Maximum columns per row
        rows = int(math.ceil(self.n_states / cols))
        
        # Adjust figure size dynamically based on the number of rows and columns
        fig, axs = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2), squeeze=False)
        axs = axs.flatten()  # Flatten for easier indexing

        for col in range(self.n_states):
            # Outer circle (full state representation)
            circleExt = patches.Circle((0.5, 0.5), 0.5, color='gray', alpha=0.1)
            axs[col].add_patch(circleExt)

            # Inner circle (amplitude-based)
            circleInt = patches.Circle((0.5, 0.5), self.prob_qubit[col] / 2, color='b', alpha=0.3)
            axs[col].add_patch(circleInt)

            # Title with state name
            state_number = f"|{col}>"
            axs[col].set_title(state_number)

            # Draw phase line
            xl = [0.5, 0.5 + 0.5 * self.prob_qubit[col] * np.cos(self.phase_qubit[col] + np.pi / 2)]
            yl = [0.5, 0.5 + 0.5 * self.prob_qubit[col] * np.sin(self.phase_qubit[col] + np.pi / 2)]
            axs[col].plot(xl, yl, 'r')

            axs[col].set_aspect('equal')
            axs[col].axis('off')
        
        # Hide unused axes
        for col in range(self.n_states, len(axs)):
            axs[col].axis('off')

        plt.tight_layout()  # Prevent overlap
        plt.show()