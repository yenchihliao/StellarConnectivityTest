import numpy as np
from Node import *
from NodeFactory import *
import DelayStrat
import ConnStrat
from Quorum import SCPQuorum
import Utils
import random
import math
import matplotlib.pyplot as plt
from simpleTest import getPriority

"""
INPUT:
    viewTargets: targets from different views.
    nodes: keep track of nodes that are supporting.
    supported: value that is seeking support
OUTPUT:
    nodes[i] = 1 if node i has supported in its viewTarget
"""
def findSupport(viewTargets, nodes, supported, count = 0):
    if(count == len(nodes)):
        return
    for targets in viewTargets:
        for i in range(len(targets)):
            if(nodes[i] == 1):
                continue
            if(targets[i] == supported):
                nodes[i] = 1
                findSupport(viewTargets, nodes, i, count+1)

if __name__ == '__main__':
    targetHeight = 10000
    y = [] # collects results for plots
    # conduct experiment with 4~100 nodes
    for NODE_COUNT in range(4, 100, 3):
        # making node instances
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
            viewTargets = []
            nominees = set()
            targets = np.zeros(NODE_COUNT)

            nextView = True
            while(nextView):
                # get the priority for this view
                for i in range(NODE_COUNT):
                    targets[i] = getPriority(i, quorums)
                    if(targets[i] == i):
                        nominees.add(i)
                viewTargets.append(targets)

                # see if ractirfied
                nodes = np.zeros(NODE_COUNT)
                suc = False
                for nominee in nominees:
                    findSupport(viewTargets, nodes, nominee)
                    if(sum(nodes) > math.floor(NODE_COUNT * 0.67)):
                        suc = True
                        break
                if(suc):
                    height += 1
                    nextView = False
                else:
                    fail += 1
        y.append(fail)
        print(height, fail)
    x = np.arange(4, 100, 3)
    print(y)
    plt.plot(x, y)
    plt.show()
