from TimeoutStrat import *
from ConnectStrat import *
from NetworkDelayStrat import *

class AbstractNodeFactory():
    def __init__(self):
        pass
    def createDelay(self):
        pass
    def createTimer(self):
        pass
    def createConn(self):
        pass

class noD_LT_UniFixConn(AbstractNodeFactory):
    def __init__(self,
        gap=1,
        peerCount=4,
        threshold=3):
        self.mDelay = NoDelay()
        self.mTimer = TimeoutLinear(gap)
        self.mQuorum = UniformFixedConn(Quroum)
    def createDelay(self):
        return self.mDelay
    def createTimer(self):
        return self.mTimer
    def createConn(self):
        return self.mQuorum
