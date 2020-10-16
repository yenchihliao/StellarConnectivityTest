from Quorum import *
from Node import *
"""
In charge of generating peers and quorum settings,
while handling broadcast strategy and following
the delay given when initializing.
"""

class AbstractConn():
    mQuorum = {}
    mPeers = {}
    def __init__(self):
        self.mDelay
    def _quorumGenerate(self):
        pass
    def getQuorum(self):
        pass
    def _send(self):
        pass
    def broadcast(self, msg):
        pass
    def ractify(self, votes, view, value):
        pass
    def VBlocking(self):
        pass
"""
Establish a uniform connected FBAS.
Only one instance is needed across multiple nodes.
initWithPeers() before delegating broadcast().
"""
class UniformConn(AbstractConn):
    mQuorum = []
    mPeers = set()
    def __init__(self, delayStrat):
        self.mDelay = delayStrat
    def initWithPeers(self, peers):
        self.mPeers = peers
        self.mCount = len(peers)
        self._quorumGenerate()
    def _quorumGenerate(self):
        threshold = 3
        for nodeID in range(self.mCount):
            sliceSet = set()
            for i in range(4):
                sliceSet.add((nodeID + i) % self.mCount)
                self.mQuorum.append(SCPQuorum(sliceSet, threshold))
    def getQuorum(self):
        return self.mQuorum
    def _send(self, msg, targetID):
        sleep(self.mDelay.getDelay(targetID))
        self.mPeers[targetID].recv(self.mNodeID, msg)
    def broadcast(self, msg):
        for peer in self.mPeers:
            t = Thread(target=self._send, args=(msg, peer))
            t.start()
    def ractify(self, votes, view, value):
        return False
    def VBlocking(self):
        pass

class UniformConn2(UniformConn):
    def _quorumGenerate(self):
        for nodeID in range(nodeCount):
            sliceSet = set()
            for i in range(4):
                sliceSet.add((nodeID + i) % self.mCount)
            threshold = 3
            tmpQuorum = SCPQuorum(sliceSet, threshold)
            sliceSet = set()
            sliceSet.add(tmpQuorum)
            for i in range(3):
                sliceSet.add((nodeID+4+i) % nodeCount)
            threshold = 3
            mQuorum.append(SCPQuorum(sliceSet, threshold))

class NonUniformFixed(UniformConn):
    def _quorumGenerate(self):
        for nodeID in range(nodeCount-2):
            sliceSet = set()
            for i in range(4):
                sliceSet.add((nodeID + i) % (nodeCount-2))
            threshold = 3
            tmpQuorum = SCPQuorum(sliceSet, threshold)
            sliceSet = set()
            sliceSet.add(tmpQuorum)
            for i in range(3):
                sliceSet.add((nodeID+4+i) % (nodeCount-2))
            threshold = 3
            mQuorum.append(SCPQuorum(sliceSet, threshold))
        mQuorums.append(SCPQuorum({1, 2, 3}, 3))
        mQuorums.append(SCPQuorum({1, 2, 3, 4, 5, 6}, 1))

if __name__ == '__main__':
    import DelayStrat
    c = UniformConn(DelayStrat.NoDelay())
    c2 = UniformConn2(DelayStrat.NoDelay())
