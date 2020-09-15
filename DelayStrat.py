class AbstractDelay():
    def __init__(self):
        pass
    def getDelay(self, nodeID):
        pass

class NoDelay(AbstractDelay):
    def __init__(self):
        pass
    def getDelay(self, nodeID):
        return 0
