"""
In charge of handling peers, quorum settings, and broadcast strategy.
"""
import DelayStrat
import BroadcastStrat

class AbstractConn():
    def __init__(self):
        self.mPeers
        self.mSlice
        self.mThreshold
        self.mBroadcast
        self.mDelay
        self.mNodeID
    def _send(self):
        pass
    def broadcast(self, msg):
        pass
    def ractify(self, votes, view):
        pass
    def VBlocking(self):
        pass
class FixedConn(AbstractConn):
    def __init__(self, nodeID, peerSet, sliceSet, threshold):
        self.mNodeID = nodeID
        self.mPeers = peerSet
        self.mSlice = sliceSet
        self.mThreshold = threshold
        self.mBroadcast = BroadcastStrat.NaiveBroadcast()
        self.mDelay = BroadcastStrat.NoDelay()
    def _send(self, msg, targetID):
        sleep(self.mDelay.getDelay(targetID))
        self.mPeers[targetID].recv(self.mNodeID, msg)
    def broadcast(self, msg):
        for peer in self.mPeers:
            t = Thread(target=self._send, args=(msg, peer))
            t.start()
    def ractify(self, votes, view):
        pass
    def VBlocking(self):
        pass
