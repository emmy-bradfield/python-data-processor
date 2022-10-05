import signal
import sched
import time
import os
import pytest
from ingest.shutdownwatcher import ShutdownWatcher
from unittest.mock import MagicMock

def teardown_function():
    import logging
    loggers = [logging.getLogger()] + \
        list(logging.Logger.manager.loggerDict.values())
    for logger in loggers:
        handlers = getattr(logger, 'handlers', [])
        for handler in handlers:
            logger.removeHandler(handler)
            
@pytest.fixture(scope='function')
def watcher():
    return ShutdownWatcher()

@pytest.mark.parametrize('sig', [signal.SIGINT, signal.SIGTERM])
def test_shutdown_manager(watcher, sig):
    assert watcher.should_continue
    
    s = sched.scheduler(time.time, time.sleep)
    s.enter(0.1, 1, lambda: os.kill(os.getpid(), sig))
    
    with watcher as w:
        s.run()
        w.serve_forever
        
    assert not watcher.should_continue