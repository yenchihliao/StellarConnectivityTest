from threading import Event, Timer
import time

class AbstractTimeout():
    def __init__(self):
        pass
    def _setEvent(self):
        pass
    def _nextTime():
        pass
    def reset(self, timeout):
        pass
    def manualReset(self, timeout):
        pass
    def fired(self):
        pass

class TimeoutLinear(AbstractTimeout):
    def __init__(self, gap):
        self.mEvent = Event()
        self.mBasicTimeout = 1
        self.mGap = gap
        self.mPreviousTimeout = 1
        self.reset(False)
    def _setEvent(self):
        self.mEvent.set()
    def _nextTime(self):
        self.mPreviousTimeout += self.mGap
        return self.mPreviousTimeout
    def reset(self, timeout):
        try:
            self.mTimer.cancel()
        except:
            pass
        if(timeout):
            self.mTimer = Timer(self._nextTime(), _setEvent)
        else:
            self.mPreviousTimeout = self.mBasicTimeout
            self.mTimer = Timer(self.mBasicTimeout, self._setEvent)
        self.mTimer.start()
    def manualReset(self, timeout):
        self.mPreviousTimeout = timeout
        self.mTimer =Timer(self.mPreviousTimeout, self._setEvent)
        self.mTimer.start()
    def fired(self):
        return self.mEvent.is_set()

if __name__ == '__main__':
    t = TimeoutLinear(gap=2)
    t.reset(timeout=False)
    print(t.fired())
    t.mTimer.join()
    print(t.fired())
