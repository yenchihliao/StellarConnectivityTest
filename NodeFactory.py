from TimeoutStrat import *
from ConnStrat import *
from DelayStrat import *
from NodeFactory import *
from Quorum import *

class AbstractNodeFactory():
    def __init__(self):
        pass
    def createDelay(self):
        pass
    def createTimer(self):
        pass
    def createConn(self):
        pass

class noDelayLinearTimeoutUniformConn(AbstractNodeFactory):
    def __init__(self, nodeID, peerSet, quorum, gap=1):
        self.mTimer = TimeoutLinear(gap)
        self.mConn = FixedConn(nodeID, peerSet, quorum, NoDelay())
    def createTimer(self):
        return self.mTimer
    def createConn(self):
        return self.mConn

if __name__ == '__main__':
    slices = {1, 2, 3, 4}
    quorum = SCPQuorum(slices, 3)
    factory = noDelayLinearTimeoutUniformConn (1, slices, quorum)
    t = factory.createTimer()
    c = factory.createConn()
