from typing import List
from ..schemas import Source

def dedupe_sources(sources: List[Source]) -> List[Source]:
    seen = set()
    out = []
    for s in sources:
        key = (s.doi or s.url or s.title).lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out
