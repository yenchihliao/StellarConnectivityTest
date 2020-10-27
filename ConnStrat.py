from Quorum import *
from Node import *
from math import ceil
from copy import deepcopy
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
    def _send(self):
        pass
    def broadcast(self, msg):
        pass
    def _satisfy(self, peer, agrees):
        pass
    def VBlocking(self):
        pass
    def ractify(self, votes, view, value):
        pass
    def getQuorum(self):
        return self.mQuorum
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
    # Feed in the instances of all nodes to use this class.
    # trustRatio is the ratio of nodes trusted in the System.
    # threshold is the ratio of a slice to the System.
    def initWithPeers(self, peers, trustRatio, thresholdRatio):
        self.mPeers = peers
        self.mCount = len(peers)
        self._quorumGenerate(trustRatio, thresholdRatio)
    def _quorumGenerate(self, trustRatio, thresholdRatio):
        print('generating quorum @ConnStrat')
        threshold = ceil(self.mCount * thresholdRatio)
        for nodeID in range(ceil(self.mCount * trustRatio)):
            sliceSet = set()
            for i in range(self.mCount):
                sliceSet.add((nodeID + i) % self.mCount)
            self.mQuorum.append(SCPQuorum(sliceSet, threshold))
            self.mQuorum[-1].show(True)
    def _send(self, msg, peer):
        sleep(self.mDelay.getDelay(peer.mNodeID))
        peer.recv(msg)
    def broadcast(self, msg):
        for peer in self.mPeers:
            t = Thread(target=self._send, args=(msg, peer))
            t.start()
    """
    INPUT: target is nodeID, and agrees is set of nodeIDs
    OUTPUT: True if agrees is a convincing slice for node, target.
    """
    def _satisfy(self, target, agrees):
        return self.mQuorum[target].satisfiedBy(agrees)
    """
    INPUT: target is nodeID, and peers is set of nodeIDs.
    OUTPUT: True if peers is a v-blocking to node, target.
    """
    def VBlocking(self, target, peers):
        return self.mQuorum[target].isBlockedBy(peers)
    """
    INPUT: view, value, and votes which maps nodeID to their highest(view) vote.
    OUTPUT: The set of nodeIDs ractifying value or False otherwise.
    """
    def ractify(self, votes, view, value):
        agrees = set()
        values = deepcopy(votes).values()
        for msg in values:
            if(msg.mView == view and msg.mVote == value):
                agrees.add(msg.mSender)
        changed = True
        while(changed):
            changed = False
            for peer in agrees:
                if(not self._satisfy(peer, agrees)):
                    agrees.remove(peer)
                    changed = True
                    break
        if(len(agrees) > 0):
            return agrees
        return False

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
