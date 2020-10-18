from TimeoutStrat import *
from ConnStrat import *
from DelayStrat import *
from NodeFactory import *

class AbstractNodeFactory():
    mConn = False
    def __init__(self):
        pass
    def createTimer(self):
        pass
    def createConn(self):
        pass
    def createLifeTime(self):
        pass

"""
Decides all the parameter in the experiment, including
the topology between nodes, message delay, and the
life time of each nodes
"""
class SimpleNodeFactory(AbstractNodeFactory):
    def __init__(self, gap=1):
        self.mGap = gap
        self.mConn = UniformConn(NoDelay())
    def createTimer(self):
        return TimeoutLinear(self.mGap)
    def createConn(self):
        return self.mConn
    def createLifeTime(self):
        return 5

if __name__ == '__main__':
    factory = SimpleNodeFactory()
    connect = UniformConn(NoDelay())
    factory.setConn(connect)
    t = factory.createTimer()
    c = factory.createConn()
    duration = factory.createLifeTime()
