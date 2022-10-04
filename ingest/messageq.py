from multiprocessing import Event, Queue
from multiprocessing.managers import BaseManager
from queue import Empty
from typing import Any, List

from ingest.debugging import app_logger as log

class QueueWrapper(object):
    
    def __init__(self, name: str, q: Queue = None, prevent_writes: Event = None):
        self.name = name
        self.q = q or Queue()
        self._prevent_writes = prevent_writes or Event()

    def get(self) -> Any:
        if self.is_drained:
            return 'STOP'
        
        try:
            return self.q.get()
        except:
            log.info('q.get() interupted')
            return 'STOP'
    
    def put(self, obj: object) -> Any:
        if self.is_writable:
            log.debug('adding message to queue')
            self.q.put(obj)
    
    def put_many(self, objs: List[object]):
        for obj in objs:
            self.put(obj)
    
    def prevent_writes(self):
        log.debug(f'preventing writes to {self.name} queue')
        self._prevent_writes.set()
    
    @property
    def is_writable(self) -> bool:
        return not self._prevent_writes.is_set
    
    @property
    def is_drained(self) -> bool:
        return not self.is_writable and self.empty
    
    @property
    def empty(self) -> bool :
        return self.q.empty
    
class QueueManager(BaseManager):
    pass

def register_manager(name: str, queue: QueueWrapper = None):
    if queue:
        QueueManager.register(name, callable=lambda : queue)
    else:
        QueueManager.register(name)

def create_queue_manager(port: int):
    return QueueManager(address=('127.0.0.1', port), authkey=b'ingestbackend')