from Node import *
from NodeFactory import *
import DelayStrat
import ConnStrat
from Quorum import SCPQuorum
import Utils

class Counter():
    lock = Lock()
    counter = 0
    sucCount = 0
    def callOnSuccess(self):
        self.lock.acquire()
        self.counter += 1
        self.lock.release()
    def clean(self):
        if(self.counter):
            self.sucCount += 1
            self.counter = 0
        return self.sucCount
if __name__ == '__main__':
    # Experiment parameters
    nodeCount = 4
    factory = SimpleNodeFactory(0.5, 0.5)
    loopCount = 10

    counter = Counter()
    while(loopCount > 0):
        print('###############################')
        # Instantiate instances with parameters
        nodes = []
        for nodeID in range(nodeCount):
            nodes.append(NodeOneShot(factory, nodeID, counter.callOnSuccess))
        factory.createConn().initWithPeers(nodes, 1, 0.67)

        # Evaluate the NodeRank
        # Utils.NodeRank(nodes[0].mConn.getQuorum(), nodeCount)

        # run the instances
        t = []
        for node in nodes:
            t.append(Thread(target=node.run))
            t[-1].start()
        for tt in t:
            tt.join()
        loopCount -= 1
        print(counter.clean())
