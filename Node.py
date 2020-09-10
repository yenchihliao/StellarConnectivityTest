from threading import Timer, Event

class Node():
    def __init__(self, factory):
        self.mFactory = factory
        self.mDelay = mFactory.createDelay()
        self.mTimer = mFactory.createTimer()
        self.mQuroum = mFactory.createConn()
        self.mView = 1
        self.mVotes = {}
    def run():
        self.mTimer.reset(False)
        while(not self.mTimer.fired()):
            if(Ratified(self.mVotes)):
                print('Ratified')
                changeView(False)
        changeView(True)
        print('timeout')
    def stop(self):
        pass
    def setPeers(self):
        pass
    def recv(self, nodeID, msg):
        if(self.mVotes[nodeID].mView >= msg.view)
    def log(self):
        pass
    def broadcast(self, msg):
        for peer in self.mPeers:
            peer.recv(msg)
    def changeView(self, timeout):
        self.view += 1
        if(timeout):
            self.mTimer.reset(True)
        else:
            self.mTimer.reset(False)
        pass
