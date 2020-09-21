from Node import Node
from NodeFactory import noDelayLinearTimeoutUniformConn
from Quorum import SCPQuorum
import numpy as np
from numpy import linalg as LA
from copy import deepcopy


def LegalTransformation(M):
    for i in range(len(M)):
        if(sum(M[:, i]) - 1 > 1e-7):
            return False
    return True

def PageRank(trustGraph, nodeCount, d = 0.85):
    matrix = deepcopy(trustGraph)
    for row in matrix:
        s = sum(row)
        if(s):
            row /= s
    matrix *= d
    matrix += np.ones((nodeCount, nodeCount)) * (1-d) / nodeCount
    # print(LegalTransformation(matrix.T))
    matrix = matrix.T
    w, v = LA.eig(matrix)
    np.set_printoptions(precision=5, linewidth=225)
    # print(v)
    v = v[:, np.argmax(w)].real
    v /= sum(v)
    return v
def NodeRank(trustGraph):
    matrix = deepcopy(trustGraph[:, :-1])
    threshold = trustGraph[:, -1]
    pass
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
    nodeCount = 8
    # Case uniform connected
    factories = []
    peerSet = set()
    for i in range(100):
        peerSet.add(i)

    trustGraph = np.zeros((nodeCount, nodeCount+1))
    for nodeID in range(nodeCount):
        for i in range(4):
            trustGraph[nodeID][(nodeID + i) % nodeCount] = 1
        trustGraph[nodeID][-1] = 3
        quorum = SCPQuorum(trustGraph[nodeID][:-1], trustGraph[nodeID][-1])
        factories.append(noDelayLinearTimeoutUniformConn(
            nodeID,
            peerSet,
            quorum))

    print(PageRank(trustGraph[:, :-1], nodeCount))
    # print(NodeRank(quorums), PageRank(quorums), QuorumIntersection(quorums))
