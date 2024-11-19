def HAD(qubit, prev_states, num_states, layer):
    edges = []
    
    # CHECK QUBIT MANIPULATED
    n_qubit = qubit[0]
    
    # |00> GREATER VALUE == LEFTMOST
    #  ^

    prev_states_count = len(prev_states)

    # CHECK STATE COMPLEXITY
    if prev_states_count < num_states:
        # States increased, create FORK
        for i in range(0, num_states // 2):
            print("Adding to state", i)
            # create edge from "itself"
            solo = {
                "start": (layer, i),
                "end": (layer + 1, i),
                "amplitude": 0,
                "phase": 0
            }
            # create the paired edge
            pair = {
                "start": (layer, i),
                "end": (layer + 1, i + num_states // 2),
                "amplitude": 0,
                "phase": 0
            }

            edges.append(solo)
            edges.append(pair)

    else:
        # Calculate stride based on the qubit manipulated (MSB = 0, LSB = n-1)
        stride = 2 ** (n_qubit)
        print("The stride is now", stride)
        
        for i in reversed(prev_states):
            # Calculate the partner state index based on stride
            partner_index = i ^ stride  # XOR to find the "partner" in the superposition
            print("State", i, "partner is", partner_index)

            # fix for XOR wraparound
            if partner_index >= i:
                join_edge = {
                    "start": (layer, i),
                    "end": (layer + 1, i),
                    "amplitude": 0,
                    "phase": 0
                }
            else:
                join_edge = {
                    "start": (layer, i),
                    "end": (layer + 1, partner_index),
                    "amplitude": 0,
                    "phase": 0
                }
            edges.append(join_edge)
    return edges