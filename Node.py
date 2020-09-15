from threading import Timer, Event, Thread
from time import sleep
from AbstractNodeFactory import *
from Messge import SCPMessage

class Node():
    mView = 1
    mVotes = {}
    mValue = ""

    def __init__(self, factory, nodeID):
        self.mNodeID = nodeID
        self.mFactory = factory
        # self.mDelay = mFactory.createDelay()
        # self.mTimer = mFactory.createTimer()
        # self.mQuorum = mFactory.createConn()
    def run(self):
        self.mTimer.set(self.changeView, False)
        self.mTimer.start()
        while(not self.mQuroum.ractify(mVotes)):
            self.mTimer.cancel()
            print('Ractified')
            self.changeView(hasTimeout=False)
    def recv(self, msg):
        # if(self.mVotes[nodeID].mView >= msg.view)
        if(self._isNewerMsg(msg)):
            mVotes[msg.mSender] = msg.mVote
        msg.show()
    def log(self):
        pass
    def broadcast(self, msg):
        self.mQuroum.broadcast(msg)
    def changeView(self, hasTimeout):
        self.view += 1
        self.mTimer.set(hasTimeout)
