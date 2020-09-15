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
    def __init__(self, func):
        self.mFunc = func
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
    mGap = gap
    mPreviousTimeout = 1
    def __init__(self, gap, func):
        self.mFunc = func
        # self.mEvent = Event()
        self.reset(False)
    # Returns the time for the next timeout
    def _nextTime(self):
        self.mPreviousTimeout += self.mGap
        return self.mPreviousTimeout
    def set(self, func, arg, hasTimeout):
        if(hasTimeout):
            self.mTimer = Timer(self._nextTime(), func, arg)
        else:
            self.mPreviousTimeout = self._mBasicTimeout
            self.mTimer = Timer(self.mBasicTimeout, self._setEvent)
        self.mTimer.start()
    def manualSet(self, func, arg, timeout):
        self.mPreviousTimeout = timeout
        self.mTimer =Timer(self.mPreviousTimeout, self._setEvent)
    def start(self):
        self.mTimer.start()
    def cancel(self):
        self.mTimer.cancel()

if __name__ == '__main__':
    t = TimeoutLinear(gap=2)
    t.reset(timeout=False)
    print(t.fired())
    t.mTimer.join()
    print(t.fired())
