import random
from threading import Timer, Event, Thread, Lock
from time import sleep
# from AbstractNodeFactory import *
from Message import SCPMessage

# In charge of protocol itself
# Network delay simulation, timeout strategy, and quorum(peers and trust)
#       are delegated to other objects
class Node():
    mView = 0
    mVoteLock = Lock() # mutex lock for accessing mVotes
    # mVotes: List<map<nodeID, vote>>, dictionaries mapping nodeID to the vote with highest view indexed by height
    mVotes = [{}]
    mNoCandidate = True # Ture if no local candidate for current view
    mValue = "" # The local candidate for current view
    mHeight = 0 # success count
    mBlocks = [] # success record
    _mEventDurationExpire = Event() # Event for ending the node(protocol)
    mLog = '' # Output string
    def __init__(self, factory, nodeID):
        self.mNodeID = nodeID
        self.mFile = open('node{}.txt'.format(self.mNodeID), 'w')
        self.mFactory = factory
        self.mTimer = self.mFactory.createTimer()
        self.mConn = self.mFactory.createConn()
        self.mDuration = self.mFactory.createLifeTime()
    """
    OUTPUT: Randomly selected peer from slices
    NOTE: Invoked by _getCandidate
    """
    def _getPriority(self):
        # nodeCount ought to be unknow variable in FBAS.
        # Used here only for convenience.
        quorum = self.mConn.getQuorum()
        vec = quorum[self.mNodeID].toVector(len(quorum))
        rand = random.randint(0, sum(vec) - 1)
        for i in range(len(vec)):
            if(rand > 0):
                rand -= vec[i]
            else:
                return i
        return len(vec)
    """
    INPUT: hasTimeout is True if this function is called in the
            case of timeout.
    Algorithm: Assign local mValue for later broadcast
    """
    def _getCandidate(self, hasTimeout, height): # acquires lock on mVote
        # self.log('node{} get target {}'.format(self.mNodeID, target))
        target = self._getPriority()
        self.log('Got candidate from {}'.format(target))
        self.mVoteLock.acquire()
        while(len(self.mVotes) <= height):
            self.mVotes.append({})
        msg = self.mVotes[height].get(target)
        if(msg):
            if(msg.mView == self.mView):
                self.mValue = msg.mVote
                self.mVoteLock.release()
                return
        self.mValue = '{}: {}, {}->{}'.format(self.mNodeID, self.mHeight, self.mView, target)
        self.mVoteLock.release()
        return
    # Check if Message is newer in terms of height and view.
    # Also make sure self.mVote has enough space for the message.
    def _isNewerMsg(self, msg): # acquires lock on mVote
        self.mVoteLock.acquire()
        while(len(self.mVotes) <= msg.mHeight):
            self.mVotes.append({})
        history = self.mVotes[msg.mHeight].get(msg.mSender)
        self.mVoteLock.release()
        if(not history):
            return True
        if(history.mView < msg.mView):
            return True
        return False
    def run(self):
        # in case node ends before others
        sleep(0.1)
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
            # Skip heights when behind a v-blocking set
            peers = set()
            self.mVoteLock.acquire()
            for h in range(len(self.mVotes)-1, self.mHeight, -1):
                for peer in self.mVotes[h]:
                    peers.add(peer)
                if(self.mConn.VBlocking(self.mNodeID, peers)):
                    self.mTimer.cancel()
                    self.log('catching up from {} to {}'.format(self.mHeight, h))
                    self.changeView(False)
                    self.mHeight = h
                    self.mTimer.start()
                    break
            self.mVoteLock.release()

            # try to get a candidate if not
            if(self.mNoCandidate):
                self._getCandidate(hasTimeout = False, height = self.mHeight)
                self.mNoCandidate = False
                message = SCPMessage(self.mNodeID, self.mHeight, self.mView, self.mValue, self.mConn.getQuorum())
                self.broadcast(message)

            if(not self.mTimer.fired()):
                self.mVoteLock.acquire()
                while(len(self.mVotes) <= self.mHeight):
                    self.mVotes.append({})
                tmp = self.mConn.ractify(self.mVotes[self.mHeight], self.mView, self.mValue)
                if(tmp):
                    self.mTimer.cancel()
                    result = ''
                    for e in tmp:
                        result += str(e) + ', '
                    self.log('Ractified: {} with {}'.format(self.mValue, result))
                    self.changeView(hasTimeout=False)
                    self.mHeight += 1
                    self.mTimer.start()
                    self.mVoteLock.release()
                    continue
                self.mVoteLock.release()
            else:
                self.log('timer fired')
                self.changeView(hasTimeout=True)
                failCount += 1
                self.mTimer.start()
        self.log('Node{} duration expired'.format(self.mNodeID))
        self.log('{}:{}'.format(failCount, self.mHeight))
        # print(self.mLog)
        self.mFile.write(self.mLog)
        self.mFile.close()
        # print('\n### Node{} log:\n{}'.format(self.mNodeID, self.mLog))
    def recv(self, msg):
        self.log('recvs from {}: {}'.format(msg.mSender, msg.mVote))
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
class NodeOneShot(Node):
    def __init__(self, factory, nodeID, func):
        super().__init__(factory, nodeID)
        self.mRecord = func
    def run(self):
        self.log('running Node{}'.format(self.mNodeID))
        # mTimer triggers view change when expired.
        # The timing of starting this timer depends on the protocol.
        self.mTimer.set(hasTimeout=False)
        self.mTimer.start()
        failed = False
        # try to get a candidate if not
        while(not self.mTimer.fired()):
            if(self.mNoCandidate):
                if(self._getCandidate(hasTimeout = False, height = self.mHeight)):
                    self.mNoCandidate = False
                    message = SCPMessage(self.mNodeID, self.mHeight, self.mView, self.mValue, self.mConn.getQuorum())
                    self.broadcast(message)
                else:
                    continue

            self.mVoteLock.acquire()
            while(len(self.mVotes) <= self.mHeight):
                self.mVotes.append({})
            tmp = self.mConn.ractify(self.mVotes[self.mHeight], self.mView, self.mValue)
            if(tmp):
                self.mTimer.cancel()
                result = ''
                for e in tmp:
                    result += str(e) + ', '
                self.log('Ractified: {} with {}'.format(self.mValue, result))
                self.mVoteLock.release()
                self.mRecord()
                self.mFile.write(self.mLog)
                print(self.mLog)
                return
            self.mVoteLock.release()
        self.log('timer fired')
        print(self.mLog)
        # print('\n### Node{} log:\n{}'.format(self.mNodeID, self.mLog))

if __name__ == '__main__':
    import NodeFactory
    import Quorum
    import DelayStrat
    import ConnStrat

    factory = NodeFactory.SimpleNodeFactory(time = 3)
    node = Node(factory, 0)
    factory.mConn.initWithPeers(set([node]), 0.8, 0.666)
    node.run()
