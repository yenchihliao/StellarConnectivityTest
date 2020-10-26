from threading import Timer, Event, Thread, Lock
from time import sleep
# from AbstractNodeFactory import *
from Message import SCPMessage

# In charge of protocol itself
# Network delay simulation, timeout strategy, and quorum(peers and trust)
#       are delegated to other objects
class Node():
    mView = 0
    # mVotes: List<map<nodeID, vote>>, dictionaries mapping nodeID to the vote with highest view indexed by height
    mVoteLock = Lock()
    mVotes = [{}]
    mNoCandidate = True
    mValue = ""
    mHeight = 0
    mBlocks = []
    def __init__(self, factory, nodeID):
        self.mNodeID = nodeID
        self.mFile = open('node{}.txt'.format(self.mNodeID), 'w')
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
    def _getCandidate(self, hasTimeout, height): # acquires lock on mVote
        import random
        # nodeCount ought to be unknow variable in FBAS.
        # Used here only for convenience.
        nodeCount = len(self.mConn.getQuorum())
        target = random.randint(0, nodeCount - 1)
        # self.log('node{} get target {}'.format(self.mNodeID, target))
        if(target == self.mNodeID):
            self.mValue = 'Node{}@({}, {})'.format(self.mNodeID, self.mHeight, self.mView)
            self.log('Got candidate from {}'.format(target))
            return True
        print('{}acquiring in getCandidate\n'.format(self.mNodeID))
        self.mVoteLock.acquire()
        if(height >= len(self.mVotes)):
            print('{}releasing\n'.format(self.mNodeID))
            self.mVoteLock.release()
            return False
        msg = self.mVotes[height].get(target)
        print('{}releasing\n'.format(self.mNodeID))
        self.mVoteLock.release()
        if(msg):
            if(msg.mView == self.mView):
                self.mValue = msg.mVote
                self.log('Got candidate from {}'.format(target))
                return True
        return False
    def _isNewerMsg(self, msg): # acquires lock on mVote
        print('{}acquiring in isNewMsg\n'.format(self.mNodeID))
        self.mVoteLock.acquire()
        while(len(self.mVotes) <= msg.mHeight):
            self.mVotes.append({})
        print('{}releasing\n'.format(self.mNodeID))
        self.mVoteLock.release()
        history = self.mVotes[self.mHeight].get(msg.mSender)
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
        self.log('running Node{}'.format(self.mNodeID))
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
                if(self._getCandidate(hasTimeout = False, height = self.mHeight)):
                    self.mNoCandidate = False
                    message = SCPMessage(self.mNodeID, self.mHeight, self.mView, self.mValue, self.mConn.getQuorum())
                    self.broadcast(message)
            # sleep(0.5)
            if(not self.mTimer.fired()):
                print('{}acquiring in run\n'.format(self.mNodeID))
                self.mVoteLock.acquire()
                while(len(self.mVotes) <= self.mHeight):
                    self.mVotes.append({})
                if(self.mConn.ractify(self.mVotes[self.mHeight], self.mView, self.mValue)):
                    self.mTimer.cancel()
                    self.log('Ractified: {}'.format(self.mValue))
                    self.changeView(hasTimeout=False)
                    self.mHeight += 1
                    self.mTimer.start()
                    print('{}releasing\n'.format(self.mNodeID))
                    self.mVoteLock.release()
                    continue
                print('{}releasing\n'.format(self.mNodeID))
                self.mVoteLock.release()
            else:
                self.log('timer fired')
                self.changeView(hasTimeout=True)
                failCount += 1
                self.mTimer.start()
        self.log('Node{} duration expired'.format(self.mNodeID))
        self.log('{}:{}'.format(failCount, self.mHeight))
        print(self.mLog)
        # print('\n### Node{} log:\n{}'.format(self.mNodeID, self.mLog))
    def recv(self, msg):
        self.log('Node{} recvs: {}'.format(self.mNodeID, msg.mVote))
        if(self._isNewerMsg(msg)):
            self.mVotes[msg.mHeight][msg.mSender] = msg
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
