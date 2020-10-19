from threading import Timer, Event, Thread
from time import sleep
# from AbstractNodeFactory import *
from Message import SCPMessage

# In charge of protocol itself
# Network delay simulation, timeout strategy, and quorum(peers and trust)
#       are delegated to other objects
class Node():
    mView = 0
    mVotes = {}
    mNoCandidate = True
    mValue = ""
    mHeight = 0
    mBlocks = []
    def __init__(self, factory, nodeID):
        self.mNodeID = nodeID
        self.mFactory = factory
        self.mTimer = self.mFactory.createTimer()
        self.mConn = self.mFactory.createConn()
        self.mDuration = self.mFactory.createLifeTime()
        self._mEventDurationExpire = Event()
        self.mLog = ''
    """
    INPUT: hasTimeout is True if this function is called in the
            case of timeout.
    OUTPUT: True if sucessfully found and assigned legal valeu to
            self.mValue, False otherwise.
    NOTE: Value is selected randomly from a peer in slice.
    """
    def _getCandidate(self, hasTimeout):
        import random
        # nodeCount ought to be unknow variable in FBAS.
        # Used here only for convenience.
        nodeCount = len(self.mConn.getQuorum())
        target = random.randint(0, nodeCount - 1)
        # self.log('node{} get target {}'.format(self.mNodeID, target))
        if(target == self.mNodeID):
            self.mValue = 'Node{}@{}'.format(self.mNodeID, self.mView)
            return True
        msg = self.mVotes.get(target)
        if(msg):
            if(msg.mView == self.mView):
                self.mValue = msg.mVote
                return True
        return False
    # TODO: correct the false use of view(should reset when height increases)
    def _isNewerMsg(self, msg):
        history = self.mVotes.get(msg.mSender)
        if(not history):
            return True
        if(history.mHeight < msg.mHeight):
            return True
        elif(history.mHeight > msg.mHeight):
            return False
        else:
            if(history.mView < msg.mView):
                return True
        return False
    def run(self):
        # timer stop the node when expired.(Experiment duation)
        timer = Timer(self.mDuration, self._mEventDurationExpire.set)
        timer.start()
        # mTimer triggers view change when expired.
        # The timing of starting this timer depends on the protocol.
        self.mTimer.set(hasTimeout=False)
        self.mTimer.start()
        failCount = 0
        while(not self._mEventDurationExpire.is_set()):
            if(self.mNoCandidate):
                if(self._getCandidate(hasTimeout = False)):
                    self.mNoCandidate = False
                    message = SCPMessage(self.mNodeID, self.mHeight, self.mView, self.mValue, self.mConn.getQuorum())
                    self.broadcast(message)
            # sleep(0.5)
            if(not self.mTimer.fired()):
                if(self.mConn.ractify(self.mVotes, self.mView, self.mValue)):
                    self.mTimer.cancel()
                    # self.log('Ractified @ {}'.format(self.mView))
                    self.changeView(hasTimeout=False)
                    self.mHeight += 1
                    self.mTimer.start()
                    continue
            else:
                # self.log('{} timer fired'.format(self.mNodeID))
                self.changeView(hasTimeout=True)
                failCount += 1
                self.mTimer.start()
        self.log('Node{} duration expired'.format(self.mNodeID))
        self.log('{}:{}'.format(failCount, self.mHeight))
        print('\n### Node{} log:\n{}'.format(self.mNodeID, self.mLog))
    def recv(self, msg):
        if(self._isNewerMsg(msg)):
            self.mVotes[msg.mSender] = msg
        # msg.show()
    def log(self, output):
        # print(output)
        self.mLog += output
        self.mLog += "\n"
    def broadcast(self, msg):
        self.mConn.broadcast(msg)
    # TODO: correct the false use of view(should reset when height increases)
    def changeView(self, hasTimeout):
        # self.log('calling view change @{}, hasTimeout: {}'.format(self.mView, hasTimeout))
        if(hasTimeout):
            self.mView += 1
        else:
            self.mView = 0
        self.mNoCandidate = True
        self.mTimer.set(hasTimeout)

if __name__ == '__main__':
    import NodeFactory
    import Quorum
    import DelayStrat
    import ConnStrat

    factory = NodeFactory.SimpleNodeFactory()
    node = Node(factory, 0)
    factory.mConn.initWithPeers(set([node]), 0.8, 0.666)
    node.run()
