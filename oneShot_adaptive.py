import numpy as np
from Node import *
from NodeFactory import *
import DelayStrat
import ConnStrat
from Quorum import SCPQuorum
import Utils
import random
import math

def getPriority(nodeID, quorums):
    vec = quorums[nodeID].toVector(len(quorums))
    # print(vec)
    rand = random.randint(0, sum(vec) - 1)
    for i in range(len(vec)):
        if(rand > 0):
            rand -= vec[i]
        else:
            return i
    return len(vec)-1

def setSet(nodes, node, setID):
    if(setID == len(nodes)):
        nodes[node] = len(nodes)
        return nodes[node]
    if(node != setID):
        nodes[node] = setSet(nodes, setID, nodes[setID])
    return nodes[node]

def runUtilHeight(targetHeight, minNode, maxNode, gap = 1, faultyRate = 0):
    # print('faulty rate of {}'.format(faultyRate))
    y = []
    # conduct experiment with 4~100 nodes
    for NODE_COUNT in range(minNode, maxNode, 3*gap):
        factory = SimpleNodeFactory(time = 100, timeoutGap = 0)
        # TODO: is this a python "bug" that reusing a existing class instead of reallocating? (mConn)
        factory.mConn.mQuorum = []
        instances = []
        for nodeID in range(NODE_COUNT):
            instances.append(Node(factory, nodeID))
        factory.createConn().initWithPeers(instances, 1, 0.67)
        quorums = instances[0].mConn.getQuorum()

        # count the successful and failed approaches up to targetHeight
        height = 0
        fail = 0
        while(height < targetHeight):
            nodes = np.arange(NODE_COUNT)
            targets = np.zeros(NODE_COUNT)
            for i in range(NODE_COUNT):
                targets[i] = getPriority(i, quorums)
                if(i < math.floor(NODE_COUNT * faultyRate /100)):
                    targets[i] = NODE_COUNT
                setSet(nodes, i, int(targets[i]))
            counts = np.zeros(NODE_COUNT+1)
            for i in range(NODE_COUNT):
                counts[setSet(nodes, i, int(nodes[i]))] += 1
            # print(nodes)
            # print(targets)
            suc = False
            for i in range(len(counts)-1):
                if(counts[i] > math.floor(NODE_COUNT * 0.67)):
                    suc = True
            if(suc):
                height += 1
            else:
                fail += 1
        y.append(fail)
        print('O:', NODE_COUNT, fail)
    return y
if __name__ == '__main__':
    targetHeight = 10000
    minNode = 48
    maxNode = 85
    rets = []
    for faultyRate in range(5, 33, 6):
        rets.append(runUtilHeight(targetHeight, minNode, maxNode, faultyRate))
    print(rets)
