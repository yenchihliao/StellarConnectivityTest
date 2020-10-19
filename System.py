from Node import *
from NodeFactory import *
import DelayStrat
import ConnStrat
from Quorum import SCPQuorum
import numpy as np
from numpy import linalg as LA
from copy import deepcopy


def LegalTransformation(M):
    for i in range(len(M)):
        if(sum(M[:, i]) - 1 > 1e-7):
            return False
    return True

"""
INPUT: Matrix M, M[i][j] > 0 if i trusts j, 0 otherwise.
       nodeCount as the total number of nodes in the system.
       d as the damping factor in the PageRank
OUTPUT: Vector V representing the PageRank in percentage. sum(V) = 1.
"""
def PageRank(M, nodeCount, d = 0.85):
    print("doing PageRank with:")
    print(M)
    matrix = deepcopy(M)
    for row in matrix:
        s = sum(row)
        if(s):
            row /= s
    matrix *= d
    matrix += np.ones((nodeCount, nodeCount)) * (1-d) / nodeCount
    # print(LegalTransformation(matrix.T))
    matrix = matrix.T
    w, v = LA.eig(matrix)
    # np.set_printoptions(precision=5, linewidth=225)
    # print(matrix)
    v = v[:, np.argmax(w)].real
    v /= sum(v) # 1-norm
    return v

"""
INPUT: Slices same as NodeRank input, and a node v.
OUTPUT: all the slices S containing v.
"""
def slicesContaining(quorum, v):
    s = []
    for sliceSet in quorum:
        if(sliceSet.includes(v)):
            s.append(sliceSet)
    return s

"""
Algorithm: Adopts PageRank to match the NodeRank definition.
INPUT: sliceSet Q, and the target node v in Q.
OUTPUT: A fraction number that adopts PageRank
"""
def adopt(Q, v):
    adoptor = Q.mThreshold/len(Q.mSlices)
    for s in Q.mSlices:
        # print(type(s))
        if(type(s) == SCPQuorum):
            if(s.includes(v)):
                return adopt(s, v) * adoptor
        else:
            if(s == v):
                return adoptor
    exit(-1)

"""
INPUT: List of sliceSetting quorum[v] as sliceSet of v
OUTPUT: N*N matrix M with M[i][j] > 0 if node i trusts j
"""
def toMatrix(quorum):
    # print('doing toMatrix')
    nodeCount = len(quorum)
    M = np.zeros((nodeCount, nodeCount))
    for i in range(nodeCount):
    #     quorum[i].show(True)
        # print(quorum[i].toVector(nodeCount))
        M[i] += quorum[i].toVector(nodeCount)
    for i in range(nodeCount):
        for j in range(nodeCount):
            if M[i][j] > 0:
                M[i][j] = 1
    # print('toMatrix result\n', M)
    return M

"""
INPUT: List of sliceSetting defined in Quorum.py.
       quorum[v] represents sliceSet of node v,
       nodeCount represents total node count in the system,
       d represents the damping factor in PageRank
OUTPUT: Vector V representing the NodeRank in percentage. sum(V) = 1
"""
def NodeRank(quorum, nodeCount, d = 0.85):
    print('doing NodeRank on')
    for i in range(nodeCount):
        quorum[i].show(True)
    NR = np.zeros(nodeCount)
    PR = PageRank(toMatrix(quorum), nodeCount, d)
    print('PageRank result:')
    print(PR)
    for v in range(nodeCount): # Nodes v
        S = slicesContaining(quorum, v)
        for Q in S: # Slice Q
            for G in Q.allMember(nodeCount): # Nodes G
                NR[v] += PR[G] * adopt(Q, v)
    NR /= sum(NR) # 1-norm
    print('NodeRank result:\n', NR)
    return NR

def QuorumIntersection(quorums):
    pass

# A = 0
# B = 1
# C = 2
# D = 3
# E = 4
# F = 5
# wikiExample = np.zeros((11, 11))
# wikiExample[B, C] = 1
# wikiExample[C, B] = 1
# wikiExample[D, A] = 1
# wikiExample[D, B] = 1
# wikiExample[E, B] = 1
# wikiExample[E, D] = 1
# wikiExample[E, F] = 1
# wikiExample[F, B] = 1
# wikiExample[F, E] = 1
# wikiExample[F+1:F+4, B] = 1
# wikiExample[F+1:F+4, E] = 1
# wikiExample[-2:, E] = 1
# print(PageRank(wikiExample, 11).real)

if __name__ == '__main__':
    # Experiment parameters
    nodeCount = 4
    factory = SimpleNodeFactory()

    nodes = []
    for nodeID in range(nodeCount):
        nodes.append(Node(factory, nodeID))
    factory.createConn().initWithPeers(nodes, 1, 0.6666)

    NodeRank(nodes[0].mConn.getQuorum(), nodeCount)

    for node in nodes:
        t = Thread(target=node.run)
        t.start()
