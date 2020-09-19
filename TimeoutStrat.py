"""
In charge of setting timeout before calling input function, func.
The timer can be start or cancel arbitrarily.
Handles the timeout pattern, too.
* Timeout pattern
* Set the timer manually
* Start timer
* Cancel timer
"""
from threading import Event, Timer
import time

class AbstractTimeout():
    def __init__(self):
        pass
    def _nextTime():
        pass
    def reset(self, timeout):
        pass
    def manualSet(self, timeout):
        pass
    def start():
        pass
    def cancel():
        pass

class TimeoutLinear(AbstractTimeout):
    _mBasicTimeout = 1
    mPreviousTimeout = 1
    def __init__(self, gap):
        print("setting linear timeout with gap = ", gap)
        self.mGap = gap
        self.mEvent = Event()
        self.set(False)
        # self.mEvent = Event()
    # Returns the time for the next timeout
    def _nextTime(self):
        self.mPreviousTimeout += self.mGap
        return self.mPreviousTimeout
    def _setEvent(self):
        self.mEvent.set()
    def set(self, hasTimeout):
        self.mEvent.clear()
        if(hasTimeout):
            self.mTimer = Timer(self._nextTime(), self._setEvent)
        else:
            self.mPreviousTimeout = self._mBasicTimeout
            self.mTimer = Timer(self._mBasicTimeout, self._setEvent)
    def manualSet(self, func, arg, timeout):
        self.mPreviousTimeout = timeout
        self.mTimer =Timer(self.mPreviousTimeout, self._setEvent)
    def fired(self):
        return self.mEvent.is_set()
    def start(self):
        self.mTimer.start()
    def cancel(self):
        self.mTimer.cancel()

if __name__ == '__main__':
    t = TimeoutLinear(gap=2)
    t.set(False)
    t.start()
    print(t.fired())
    t.mTimer.join()
    print(t.fired())
    t.set(True)
    t.start()
    t.mTimer.join()
    print(t.fired())
