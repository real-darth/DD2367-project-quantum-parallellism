from qiskit import QuantumCircuit

def MCZ(qc, controls, target):
    """
    Creates a multi-control-z gate.
    
    Parameters:
        qc (QuantumCircuit): The qiskit circuit to add gate to 
        controls (list): The control qubits.
        target (int): The target qubit.
    """
    qubits = qc.num_qubits # get amount of qubits form circuit
    sub_circuit = QuantumCircuit(qubits, name="MCZ") 
    sub_circuit.h(0)                    # Convert Z on |target> to an X-equivalent
    sub_circuit.mcx(controls, target)   # Multi-controlled X
    sub_circuit.h(0)
    mcz = sub_circuit.to_instruction(label="multi-cz")
    # append correctly, with all qubits being applied
    qc.append(mcz, list(range(qubits)))