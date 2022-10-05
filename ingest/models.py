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
        return self.publication.strip().lower()
    
    def _transform_for_database(self, top_n: int):
        for word, count in self.entities.most_common(top_n):
            yield self.pub_key, 'ent', str(hash(word)), {'word': word, 'count': count}
        yield self.pub_key, None, None, {'count': self.article_count}
    
    def transform_for_database(self, top_n=2000):
        return list(self._transform_for_database(top_n))
    
    def __add__(self, other):
        self.article_count += 1
        self.publication = other.publication
        self.entities += other.entities
        return self