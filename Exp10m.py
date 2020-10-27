from Node import *
from NodeFactory import *
import DelayStrat
import ConnStrat
from Quorum import SCPQuorum
import Utils


if __name__ == '__main__':
    # Experiment parameters
    nodeCount = 4
    factory = SimpleNodeFactory()

    # Instantiate instances with parameters
    nodes = []
    for nodeID in range(nodeCount):
        nodes.append(Node(factory, nodeID))
    factory.createConn().initWithPeers(nodes, 1, 0.67)

    # Evaluate the NodeRank
    Utils.NodeRank(nodes[0].mConn.getQuorum(), nodeCount)

    # run the instances
    for node in nodes:
        t = Thread(target=node.run)
        t.start()
