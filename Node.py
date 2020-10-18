from threading import Timer, Event, Thread
from time import sleep
# from AbstractNodeFactory import *
from Message import SCPMessage

# In charge of protocol itself
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
        self.mDuration = self.mFactory.createLifeTime()
        self._mEventDurationExpire = Event()
        self.mLog = ''
    def _getCandidate(self, hasTimeout): # TODO
        return 1
    def _isNewerMsg(msg): # TODO
        pass
    def run(self):
        timer = Timer(self.mDuration, self._mEventDurationExpire.set)
        timer.start()
        self.mTimer.set(hasTimeout=False)
        self.mTimer.start()
        while(not self._mEventDurationExpire.is_set()):
            sleep(0.5)
            if(not self.mTimer.fired()):
                self.log('{} waiting ractified statement'.format(self.mNodeID))
                if(self.mConn.ractify(self.mVotes, self.mView, self.mValue)):
                    self.mTimer.cancel()
                    self.log('Ractified @ {}'.format(self.mView))
                    self.changeView(hasTimeout=False)
                    self.mTimer.start()
                    continue
            else:
                self.log('{} timer fired'.format(self.mNodeID))
                self.changeView(hasTimeout=True)
                self.mTimer.start()
        self.log('Node{} duration expired'.format(self.mNodeID))
        print(self.mLog)
    def recv(self, msg):
        # if(self.mVotes[nodeID].mView >= msg.view)
        if(self._isNewerMsg(msg)):
            mVotes[msg.mSender] = msg.mVote
        msg.show()
    def log(self, output):
        # print(output)
        self.mLog += output
        self.mLog += "\n"
    def broadcast(self, msg):
        self.mConn.broadcast(msg)
    def changeView(self, hasTimeout):
        self.log('calling view change @{}, hasTimeout: {}'.format(self.mView, hasTimeout))
        self.mView += 1
        self.mValue = self._getCandidate(hasTimeout)
        self.mTimer.set(hasTimeout)

# TODO: original object modified
if __name__ == '__main__':
    import NodeFactory
    import Quorum
    import DelayStrat
    import ConnStrat
    nodeID = 1
    peers = {1, 2, 3, 4}
    factory = NodeFactory.SimpleNodeFactory()
    factory.createConn().initWithPeers(peers)
    node = Node(factory, nodeID)
    node.run()
