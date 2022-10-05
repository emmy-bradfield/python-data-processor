from concurrent.futures import process
import os
from queue import Queue
import signal
from collections import defaultdict
from multiprocessing import Process
from typing import Dict, List, Tuple 

from .debugging import app_logger as log 
from .messageq import QueueWrapper, create_queue_manager, register_manager
from .models import ProcessedPost
from .persistance import get_database_client, persist, persist_no_op
from .processor import DataProcessor
from .shutdown import ShutdownWatcher

class Worker(Process):
    
    def __init__(self, inq: QueueWrapper, outq: QueueWrapper, cache_size: int = 25_000):
        self.iq: QueueWrapper = inq
        self.oq: QueueWrapper = outq
        super(Worker, self).__init__()
    
    def shutdown(self, *args):
        log.info('shutting down worker')
        self.iq.q.put('STOP')
    
    def count(self, incr_num: int = None):
        return 0
    
    def reset_cache(self):
        pass
    
    def cache(self, msg: ProcessedPost):
        return 0
    
    def flush_cache(self):
        pass
    
    def run(self):
        signal.signal(signal.SIGTERM, self.shutdown)
        processor = DataProcessor()
        for msg in iter(self.iq.get, 'STOP'):
            self.oq.put(processor.process(msg))
        exit(0)
        
class Saver(Process):
    
    def __init__(self, q: QueueWrapper, client, persist_fn):
        assert callable(persist_fn)
        self.q: QueueWrapper = q
        self.client = client
        self.persist_fn = persist_fn
    
    def shutdown(self, *args):
        log.info('shutting down saver')
        self.q.q.put('STOP')
    
    def run(self):
        signal.signal(signal.SIGTERM, self.shutdown)
        for msg in iter(self.iq.get, 'STOP'):
            self.persist_fn(self.client, *msg )
            
def start_processes(proc_num: int, proc: Process, proc_args: List[object]):
    log.info(f"initialising {proc_num} worker process(es)")
    procs = [proc(*proc_args) for _ in range(proc_num)]
    for p in procs:
        p.start()
    return procs

def shutdown(q: QueueWrapper, procs: List[Process]):
    q.prevent_writes()
    log.info('sending SIGTERM to processes')
    [os.kill(p.pid, signal.SIGTERM) for p in procs]
    log.info('joining processes')
    [p.join for p in procs]

def register_shutdown_handlers(queues, processes):
    def shutdown_gracefully():
        for args in zip(queues, processes):
            shutdown(*args)
    import atexit
    atexit.register(shutdown_gracefully)

def main():
    pcount = (os.cpu_count() -1) or 1
    parse_arguments = [
        ('--iproc_num', {'help': 'number of input queue workers', 'default': pcount, 'type': int})
        ('--oproc_num', {'help': 'number of output queue workers', 'default': pcount, 'type': int})
        ('--iport', {'help': 'input queue port cross proc messaging', 'default': 50_000, 'type': int})
        ('--no_persistance', {'help': 'disable database persistance', 'action': 'store_true'})
        ('--agg_cache_size', {'help': 'aggregator cache size', 'default': 25_000, 'type': int})
    ]
    