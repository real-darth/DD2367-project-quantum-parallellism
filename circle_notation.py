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
        # calculate amplitude and phase
        # calculate the amplitude and phase of the states
        self.prob_qubit = np.absolute(self.qubit)
        self.phase_qubit = np.angle(self.qubit)
        # viz par
        rows = int(math.ceil(self.n_states / 8.0))
        cols = min(self.n_states, 8)
        fig, axs = plt.subplots(rows, cols)

        #cols_limit = cols / 2
        #temp = int(cols_limit)

        for col in range(cols):
            # amplitude area
            circleExt = matplotlib.patches.Circle((0.5, 0.5), 0.5, color='gray',alpha=0.1)
            circleInt = matplotlib.patches.Circle((0.5, 0.5), self.prob_qubit[col]/2, color='b',alpha=0.3)
            axs[col].add_patch(circleExt)
            axs[col].add_patch(circleInt)
            axs[col].set_aspect('equal')

            #if (col >= cols_limit):
            #    state_number = "| -" + str(temp) + ">"
            #    temp -= 1
            #else:
            state_number = "|" + str(col) + ">"

            axs[col].set_title(state_number)
            xl = [0.5, 0.5 + 0.5*self.prob_qubit[col]*math.cos(self.phase_qubit[col] + np.pi/2)]
            yl = [0.5, 0.5 + 0.5*self.prob_qubit[col]*math.sin(self.phase_qubit[col] + np.pi/2)]
            axs[col].plot(xl,yl,'r')
            axs[col].axis('off')
        plt.show()