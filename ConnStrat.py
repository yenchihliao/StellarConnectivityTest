"""
In charge of handling peers, quorum settings,
and broadcast strategy. Also, the simulated
network delay.
"""

class AbstractConn():
    def __init__(self):
        self.mPeers
        self.mQuorum
        self.mDelay
        self.mNodeID
    def _send(self):
        pass
    def broadcast(self, msg):
        pass
    def ractify(self, votes, view, value):
        pass
    def VBlocking(self):
        pass
class FixedConn(AbstractConn):
    def __init__(self, nodeID, peerSet, quorum, delayStrat):
        self.mNodeID = nodeID
        self.mPeers = peerSet
        self.mQuorum = quorum
        self.mDelay = delayStrat
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

if __name__ == '__main__':
    import DelayStrat
    import Quorum
    c = FixedConn(1, {1, 2, 3, 4}, Quorum.SCPQuorum({1, 2, 3, 4}, 3), DelayStrat.NoDelay())
