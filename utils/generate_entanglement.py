# given a list of vertices, generate
# a list of pairs where two nodes in a
# pair are entangled qubits

from math import log2, ceil
from random import random
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import RYGate
from numpy import arcsin, sqrt

backend = Aer.get_backend("qasm_simulator")


def get_off_index(size):
    if size == 1:
        return 0

    qc = QuantumCircuit(size)

    # make the arbitrary W - state
    angle = 2 * arcsin(sqrt(1 / size))
    qc.ry(angle, 0)

    for i in range(1, size):
        angle = 2 * arcsin(sqrt(1 / (size - i)))
        gate = RYGate(angle).control(num_ctrl_qubits=i, ctrl_state=0)
        qc.compose(gate, inplace=True)

    qc.measure_all()
    # print(qc.draw())

    counts = (
        execute(qc, backend=backend, shots=1, seed_simulator=int(1000 * random()))
        .result()
        .get_counts()
    )
    # print(counts)
    key = list(counts.keys())[0]

    for i, bit in enumerate(key):
        if bit == "1":
            return i


def get_index(n):
    size = ceil(log2(n))

    qc = QuantumCircuit(size)
    qc.h(range(size))
    qc.measure_all()

    counts = (
        execute(qc, backend=backend, shots=150, seed_simulator=int(1000 * random()))
        .result()
        .get_counts()
    )

    sorted_count = sorted(counts.items(), key=lambda k: k[1], reverse=True)
    keys = sorted_count[0][0], sorted_count[1][0]

    return int(keys[0], 2) % n, int(keys[1], 2) % n


def generate_pairs(inp_vertices):
    """Generates the list of pairs"""
    n = len(inp_vertices)

    ans = {"pair_list": [], "left_out": []}
    if n % 2 == 1:
        index = get_off_index(n)
        # leave out this particular index in the list
        ans["left_out"] = inp_vertices[index]
        del inp_vertices[index]

    # now calculate the entanglement

    # try hadamards
    while inp_vertices != []:
        # for the indices
        index1, index2 = get_index(len(inp_vertices))

        # for the pairing
        qc = QuantumCircuit(2)
        qc.h(range(2))
        qc.measure_all()
        counts = (
            execute(qc, backend=backend, shots=1, seed_simulator=int(1000 * random()))
            .result()
            .get_counts()
        )

        key = list(counts.keys())[0]

        if key[0] == key[1]:
            # pair them
            ans["pair_list"].append((inp_vertices[index1], inp_vertices[index2]))
            copy_list = []
            for i in range(len(inp_vertices)):
                if i != index1 and i != index2:
                    copy_list.append(inp_vertices[i])

            inp_vertices = copy_list
        else:
            continue

    return ans


# l = [1, 2, 6, 5, 3, 8]

# print(generate_pairs(l))
