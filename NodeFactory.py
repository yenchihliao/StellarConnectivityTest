from TimeoutStrat import *
from ConnStrat import *
from DelayStrat import *
from NodeFactory import *

class AbstractNodeFactory():
    def __init__(self):
        pass
    def createDelay(self):
        pass
    def createTimer(self):
        pass
    def createConn(self):
        pass

class SimpleNodeFactory(AbstractNodeFactory):
    def __init__(self, gap=1):
        self.mGap = gap
    def createTimer(self):
        return TimeoutLinear(self.mGap)
    def createConn(self):
        return UniformConn(NoDelay())

if __name__ == '__main__':
    factory = SimpleNodeFactory()
    t = factory.createTimer()
    c = factory.createConn()
    factory.createDelay()
