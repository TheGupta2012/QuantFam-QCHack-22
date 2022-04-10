# -*- coding: utf-8 -*-
"""
Module to find the chromatic number of a graph.

"""

import numpy as np
import networkx as nx
from qiskit import Aer
from qiskit.quantum_info import Pauli
from qiskit.opflow import PauliSumOp
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA, SPSA, ADAM


def get_operator(G):
    """Construct the cost Hamiltonian for the maximum independent set of a 
    a graph defined as:
        0.5 \sum_{i=nodes} Z_i + A/4 \sum_{ij = edges} Z_i x Z_j - Z_i - Z_j.
    Args:
        class graph (networkx): the graph in networkx.
    Returns:
        dict: dictionary of pauli Z matrices and its position.
    """
    
    A = 2.6
    num_nodes = G.number_of_nodes()
 
    pauli_list = []
    
    for i in range(num_nodes):
        x_p = np.zeros(num_nodes, dtype=bool)
        z_p = np.zeros(num_nodes, dtype=bool)
        z_p[i] = True 
        pauli_list.append([1/2,Pauli((z_p,x_p))])
        
    for pair in G.edges:
        x_p = np.zeros(num_nodes, dtype=bool)
        z_p = np.zeros(num_nodes, dtype=bool)
        z_p[pair[0]] = True
        z_p[pair[1]] = True
        pauli_list.append([A/4, Pauli((z_p,x_p))])
        
    for pair in G.edges:
        x_p = np.zeros(num_nodes, dtype=bool)
        z_p = np.zeros(num_nodes, dtype=bool)
        z_p[pair[0]] = True
        pauli_list.append([-A/4, Pauli((z_p,x_p))])
        
    for pair in G.edges:
        x_p = np.zeros(num_nodes, dtype=bool)
        z_p = np.zeros(num_nodes, dtype=bool)
        z_p[pair[1]] = True
        pauli_list.append([-A/4, Pauli((z_p,x_p))])
        
    pauli_list = [(pauli[1].to_label(), pauli[0]) for pauli in pauli_list]
    
    return PauliSumOp.from_list(pauli_list)


def sample_most_likely(state_vector):
    """Compute the most likely binary string from state vector.
    Args:
        state_vector (numpy.ndarray): state vector or counts.
    Returns:
        numpy.ndarray: binary string as numpy.ndarray of ints.
    """
    n = int(np.log2(state_vector.shape[0]))
    k = np.argmax(np.abs(state_vector))
    x = np.zeros(n)
    for i in range(n):
       x[i] = k % 2
       k >>= 1
    return x
    
def max_clique(G):
    """Compute the QAOA algorithm and find the maximum independent set 
    of the graph G.
    Args:
        class graph (networkx): the graph in networkx.
    Returns:
        numpy.ndarray: binary string as numpy.ndarray of ints.
    """
    qubit_op = get_operator(G)
    optimizer = ADAM()
    qaoa = QAOA(optimizer, quantum_instance=Aer.get_backend('statevector_simulator'))

    result = qaoa.compute_minimum_eigenvalue(qubit_op)
                
    return sample_most_likely(result.eigenstate)


def chromatic_number(G):
    """Compute the chromatic number of a graph G.
    Args:
        class graph(networkx): the graph in networkx.
    Returns:
        int: integer ranging from 1 to number of nodes.  
    """
    color = 1
    while bool(G.edges):
        clique = max_clique(G)
        for i in range(len(clique)):
            if clique[i] == 1:
                G.remove_node(i)
        G=nx.convert_node_labels_to_integers(G) #relabel nodes starting from 0
        color += 1
    return color 

