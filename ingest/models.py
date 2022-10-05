from collections import Counter
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel

class Post(BaseModel):
    content: str #Required
    publication: str #Required

class ProcessedPost(BaseModel):
    publication: str
    entities: Counter = Counter()
    article_count: int = 0
    
    @property
    def pub_key(self):
        return None
    
    def transform_for_database(self, top_n=200):
        return None
    
    def __add__(self, other):
        return self