from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, nbIter = -1, functionEnd = None):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.nbIter = nbIter
        self.fctEnd = functionEnd
        self.is_running = False
        self.start()

    def _run(self):
        if (self.nbIter != -1 and self.nbIter > 0):
            self.is_running = False
            self.start()
            self.function()
            self.nbIter -= 1
        else:
            self.fctEnd()
            self.stop()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False