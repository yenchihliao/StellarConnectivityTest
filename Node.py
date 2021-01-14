import random
from threading import Timer, Event, Thread, Lock
from time import sleep
# from AbstractNodeFactory import *
from Message import SCPMessage

class AbstractNode():
    mView = 0
    mVoteLock = Lock() # mutex lock for accessing mVotes
    # mVotes: List<map<nodeID, vote>>, dictionaries mapping nodeID to the vote with highest view indexed by height
    mVotes = [{}]
    mValue = 0 # The local candidate(target) for current view
    mHeight = 0 # success count
    mBlocks = [] # success record
    _mEventDurationExpire = Event() # Event for ending the node(protocol)
    mLog = '' # Output string
    def __init__(self):
        pass
    def _getPriority(self):
        pass
    def _getCandidate(self):
        pass
    def _isNewerMsg(self):
        pass
    def run(self):
        pass
    def log(self, output):
        # print(output)
        self.mLog += output
        self.mLog += "\n"
    def broadcast(self, msg):
        self.mConn.broadcast(msg)
    def changeView(self, hasTimeout):
        pass
"""
Node is in charge of protocol itself.
1. Network delay simulation, timeout strategy, and quorum(peers and trust)
      are delegated to other objects
2. The timer start right after viewChange happens.
3. The candidate is randomly choosed within local slices.
"""
class Node(AbstractNode):
    def __init__(self, factory, nodeID):
        self.mNodeID = nodeID
        # self.mFile = open('node{}.txt'.format(self.mNodeID), 'w')
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
        # print('candidate acquired')
        while(len(self.mVotes) <= height):
            self.mVotes.append({})
        msg = self.mVotes[height].get(target)
        if(msg):
            if(msg.mView == self.mView):
                self.mValue = msg.mVote
                # print('candidate releasing')
                self.mVoteLock.release()
                return
        self.mValue = target# '{}: {}, {}->{}'.format(self.mNodeID, self.mHeight, self.mView, target)
        # print('candidate releasing')
        self.mVoteLock.release()
        return
    # Check if Message is newer in terms of height and view.
    # Also make sure self.mVote has enough space for the message.
    def _isNewerMsg(self, msg): # acquires lock on mVote
        self.mVoteLock.acquire()
        # print('newMsg acquired')
        while(len(self.mVotes) <= msg.mHeight):
            self.mVotes.append({})
        history = self.mVotes[msg.mHeight].get(msg.mSender)
        self.mVoteLock.release()
        if(not history):
            return True
        if(history.mView < msg.mView):
            return True
        return False
    """
    INPUT:
        map: nodeID-> newestVotes, topology
        the starting nodeID for traversing, start
    OUTPUT: nodeID of the target of the node start if
        legal(on the same view) vote exists. -1
        otherwise
    """
    def _goNext(self, topology, start):
        ret = topology.get(start)
        if(ret and ret.mView == self.mView):
            return int(ret.mVote)
        else:
            return -1
    """
    INPUT:
        map: nodeID-> newestVotes, topology
        the starting nodeID for traversing, start
    OUTPUT: NONE
    Algorithm:
        modify topology s.t. votes vote toward the
        ultimate target(minimum nodeID if loop exists)
    """
    def _hareTortoise(self, topology, start):
        # print("beginning of hare tortoise")
        # see if loop exists
        tortoise = self._goNext(topology, start)
        hare  = self._goNext(topology, self._goNext(topology, start))
        if(tortoise == -1):
            return
        hasLoop = True
        while(tortoise != hare):
            if(self._goNext(topology, tortoise) == -1):
                hasLoop = False
                break
            tortoise = self._goNext(topology, tortoise)
            hare  = self._goNext(topology, self._goNext(topology, hare))

        target = tortoise
        if(hasLoop):
            # find the beginning of the loop, loopStart
            loopStart = start
            while(loopStart != tortoise):
                tortoise = self._goNext(topology, tortoise)
                loopStart = self._goNext(topology, loopStart)
            # find the lowest target in the loop, target
            newTortoise = self._goNext(topology, loopStart)
            while(newTortoise != loopStart):
                if(topology[newTortoise].mVote < topology[target].mVote):
                    target = newTortoise
                newTortoise = self._goNext(topology, newTortoise)
            # assign all the target to the final ones
            newTortoise = start
            while(newTortoise != loopStart):
                nextStep = self._goNext(topology, newTortoise)
                topology[newTortoise].mVote = target
                newTortoise = nextStep
            topology[newTortoise].mVote = target
            newTortoise = self._goNext(topology, newTortoise)
            while(newTortoise != loopStart):
                nextStep = self._goNext(topology, newTortoise)
                topology[newTortoise].mVote = target
                newTortoise = nextStep
        else:
            # assign all the target to the final ones
            newTortoise = start
            while(newTortoise != tortoise):
                if(newTortoise != self._goNext(topology, newTortoise)):
                    topology[newTortoise].mVote = target
                    newTortoise = self._goNext(topology, newTortoise)
        # print("ending of hare tortoise")


    def _modifyVotes(self):
        self.mVoteLock.acquire()
        # print('modify acquired')
        # Nothing received to be modified
        if(len(self.mVotes) <= self.mHeight):
            self.mVoteLock.release()
            return
        votes = self.mVotes[self.mHeight]
        for nodeID in votes.keys():
            self._hareTortoise(votes, nodeID)
            # if(self._extractTarget(v.mVote) != v.mTarget):

        self.mVoteLock.release()

    def run(self):
        self.log('running Node{}'.format(self.mNodeID))
        # timer stop the node when expired.(Experiment duation)
        # timer = Timer(self.mDuration, self._mEventDurationExpire.set)
        # timer.start()
        # mTimer triggers view change when expired.
        # The timing of starting this timer depends on the protocol.
        self._getCandidate(hasTimeout = False, height = self.mHeight)
        message = SCPMessage(self.mNodeID, self.mHeight, self.mView, self.mValue, self.mConn.getQuorum())
        self.broadcast(message)
        self.mTimer.set(hasTimeout=False)
        self.mTimer.start()
        failCount = 0
        # while(not self._mEventDurationExpire.is_set()):
        while(self.mHeight < self.mDuration):
            # Skip heights when behind a v-blocking set
            peers = set()
            for h in range(len(self.mVotes)-1, self.mHeight, -1):
                for peer in self.mVotes[h]: # for dictionary keys, which is int(sender nodeID)
                    peers.add(peer)
                if(self.mConn.VBlocking(self.mNodeID, peers)):
                    self.mTimer.cancel()
                    self.log('catching up from {} to {}'.format(self.mHeight, h))
                    self.changeView(False)
                    self.mVoteLock.acquire()
                    print('jump to {}'.format(h))
                    self.mHeight = h
                    self.mVoteLock.release()
                    self.mTimer.start()
                    break
            # Check if any message is ractified
            if(not self.mTimer.fired()):
                if(self.mHasNewMsg):
                    self.mHasNewMsg = False
                    self.mVoteLock.acquire()
                    while(len(self.mVotes) <= self.mHeight):
                        self.mVotes.append({})
                    agrees = set()
                    for msg in self.mVotes[self.mHeight].values():
                        if(msg.mView == self.mView and msg.mVote == self.mValue):
                            agrees.add(msg.mSender)
                    tmp = self.mConn.ractify(agrees)
                    self.mVoteLock.release()
                    if(tmp):
                        self.mTimer.cancel()
                        result = ''
                        for e in tmp:
                            result += str(e) + ', '
                        self.log('Ractified: {} with {}'.format(self.mValue, result))
                        self.changeView(hasTimeout=False)
                        self.mTimer.start()
                        continue
            else:
                self.log('timer fired')
                self.changeView(hasTimeout=True)
                failCount += 1
                self.mTimer.start()
        self.log('Node{} duration expired'.format(self.mNodeID))
        self.log('{}:{}'.format(failCount, self.mHeight))
        # print(self.mLog)
        # self.mFile.write(self.mLog)
        # self.mFile.close()
        # print('\n### Node{} log:\n{}'.format(self.mNodeID, self.mLog))
    def recv(self, msg):
        self.log('recvs from {}({}, {}) -> {}'.format(msg.mSender, msg.mHeight, msg.mView,  msg.mVote))
        if(self._isNewerMsg(msg)):
            self.mVotes[msg.mHeight][msg.mSender] = msg
        # Modify mVotes according to target
        # Only needed in this protocol
        self._modifyVotes()
        if(msg.mHeight == self.mHeight and msg.mView == self.mView):
            self.mHasNewMsg = True
    def changeView(self, hasTimeout):
        # self.log('calling view change @{}, hasTimeout: {}'.format(self.mView, hasTimeout))
        if(hasTimeout):
            self.mView += 1
        else:
            self.mView = 0
            self.mHeight += 1
        self._getCandidate(hasTimeout = False, height = self.mHeight)
        message = SCPMessage(self.mNodeID, self.mHeight, self.mView, self.mValue, self.mConn.getQuorum())
        self.broadcast(message)
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

            if(self.mHasNewMsg):
                self.mHasNewMsg = False
                self.mVoteLock.acquire()
                while(len(self.mVotes) <= self.mHeight):
                    self.mVotes.append({})
                agrees = set()
                for msg in self.mVotes[self.mHeight].values():
                    if(msg.mView == self.mView and msg.mVote == self.mValue):
                        agrees.add(msg.mSender)
                tmp = self.mConn.ractify(agrees)
                if(tmp):
                    self.mTimer.cancel()
                    result = ''
                    for e in tmp:
                        result += str(e) + ', '
                    self.log('Ractified: {} with {}'.format(self.mValue, result))
                    self.mVoteLock.release()
                    self.mRecord()
                    # self.mFile.write(self.mLog)
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
