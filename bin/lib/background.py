import threading

class Background:

    class Runner(threading.Thread):
        def __init__(self, callback, period_ms):
            self.callback = callback
            self.period_ms = period_ms
            self.stopped = False
            threading.Thread.__init__(self)

        def run(self):
            b = threading.Barrier(2)
            def unblock():
                b.wait()
            while not self.stopped:
                print("running callback")
                self.callback()
                threading.Timer(period_ms/1000, unblock)
                b.wait()

    def __init__(self, period_ms, callback, **callback_kwargs):
        self.callback = callback
        self.kwargs = callback_kwargs
        self.kwargs_lock = threading.Lock()
        self.runner = Background.Runner(self.CallbackWrapper, period_ms)
        self.runner.start()

    def SetCallbackKwargs(self, **kwargs):
        with self.kwargs_lock:
            self.kwargs.update(kwargs)

    def CallbackWrapper(self):
        with self.kwargs_lock:
            self.callback(**(self.kwargs))

