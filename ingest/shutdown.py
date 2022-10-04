import signal
import time
from .debugging import app_logger as log

class ShutdownWatcher:
    
    def __init__(self):
        self.should_continue = True
        
        for s in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(s, self.exit)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.exit()
    
    def serve_forever(self):
        while self.should_continue == True:
            time.sleep(0.1)
    
    def exit(self, *args, **kwargs):
        self.should_continue = False