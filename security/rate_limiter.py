from collections import defaultdict, deque
from time import time
from fastapi import HTTPException, status, Request


def parse_rate(rate: str) -> tuple[int, int]:
    count, _, period = rate.partition("/")
    count = int(count)
    seconds = 60 if period.startswith("minute") else 3600
    return count, seconds


class RateLimiter:
    def __init__(self, rate: str):
        self.limit, self.window = parse_rate(rate)
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str):
        now = time()
        q = self.hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.limit:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        q.append(now)

    async def middleware(self, request: Request, call_next):
        key = request.client.host if request.client else "anonymous"
        self.check(key)
        return await call_next(request)
