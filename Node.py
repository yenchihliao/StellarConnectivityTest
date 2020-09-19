from threading import Timer, Event, Thread
from time import sleep
# from AbstractNodeFactory import *
from Message import SCPMessage

# In charge of protocol it self
# Network delay simulation, timeout strategy, and quorum(peers and trust)
#       are delegated to other objects
class Node():
    mView = 1
    mVotes = {}

    def __init__(self, factory, nodeID):
        self.mNodeID = nodeID
        self.mFactory = factory
        self.mValue = self._getCandidate(False) # TODO
        self.mTimer = self.mFactory.createTimer()
        self.mConn = self.mFactory.createConn()
    def _getCandidate(self, hasTimeout): # TODO
        return 1
    def _isNewerMsg(msg): # TODO
        pass
    def run(self):
        self.mTimer.set(hasTimeout=False)
        self.mTimer.start()
        while(True):
            sleep(0.5)
            if(not self.mTimer.fired()):
                print('N')
                if(self.mConn.ractify(self.mVotes, self.mView, self.mValue)):
                    self.mTimer.cancel()
                    print('Ractified', '@', self.mView)
                    self.changeView(hasTimeout=False)
                    self.mTimer.start()
                    continue
            else:
                print('Y')
                self.changeView(hasTimeout=True)
                self.mTimer.start()
    def recv(self, msg):
        # if(self.mVotes[nodeID].mView >= msg.view)
        if(self._isNewerMsg(msg)):
            mVotes[msg.mSender] = msg.mVote
        msg.show()
    def log(self):
        pass
    def broadcast(self, msg):
        self.mConn.broadcast(msg)
    def changeView(self, hasTimeout):
        print('calling view change @', self.mView, hasTimeout)
        self.mView += 1
        self.mValue = self._getCandidate(hasTimeout)
        self.mTimer.set(hasTimeout)

if __name__ == '__main__':
    import NodeFactory
    import Quorum
    nodeID = 1
    peers = {1, 2, 3, 4}
    quorum = Quorum.SCPQuorum(peers, 3)
    node = Node(NodeFactory.noDelayLinearTimeoutUniformConn(
        nodeID, peers, quorum), nodeID)
    node.run()
