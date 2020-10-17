from TimeoutStrat import *
from ConnStrat import *
from DelayStrat import *
from NodeFactory import *

class AbstractNodeFactory():
    mConn = False
    def __init__(self):
        pass
    def setConn(self):
        pass
    def createTimer(self):
        pass
    def createConn(self):
        pass

class SimpleNodeFactory(AbstractNodeFactory):
    def __init__(self, gap=1):
        self.mGap = gap
        self.mConn = False
    def setConn(self, connect):
        self.mConn = connect
    def createTimer(self):
        return TimeoutLinear(self.mGap)
    def createConn(self):
        return self.mConn

if __name__ == '__main__':
    factory = SimpleNodeFactory()
    connect = UniformConn(NoDelay())
    factory.setConn(connect)
    t = factory.createTimer()
    c = factory.createConn()
