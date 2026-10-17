"""Sliding-window rate limiter -- log (exact, O(limit) per key) vs counter (approximate, O(1) per key); multi-granularity keys; idle-key eviction."""
from collections import deque
from random import Random

# --- solution ---
class SlidingWindowLog:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.logs = {}                                    # key -> deque of accepted timestamps (at most `limit` of them)

    def peek(self, key, now):
        log = self.logs.get(key)
        while log and log[0] <= now - self.window:        # window is (now - window, now]
            log.popleft()
        return len(log or ()) < self.limit

    def record(self, key, now):
        self.logs.setdefault(key, deque()).append(now)

class SlidingWindowCounter:
    """Two fixed buckets blended: count = prev * (1 - elapsed/window) + cur. Memory: two integers per key."""
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.state = {}                                   # key -> [bucket_start, cur, prev]

    def _roll(self, key, now):
        start = now - now % self.window
        s = self.state.setdefault(key, [start, 0, 0])
        if start != s[0]:
            s[2] = s[1] if start - s[0] == self.window else 0     # skipped a whole bucket => prev is empty
            s[1], s[0] = 0, start
        return s, (now - start) / self.window

    def peek(self, key, now):
        s, frac = self._roll(key, now)
        return s[2] * (1 - frac) + s[1] < self.limit

    def record(self, key, now):
        self._roll(key, now)[0][1] += 1

class RateLimiter:
    def __init__(self, rules, make=SlidingWindowLog):
        self.rules = {name: make(limit, window) for name, (limit, window) in rules.items()}

    def allow(self, request, now):
        keys = [(name, request[name]) for name in self.rules if name in request]   # one key per granularity
        if not all(self.rules[name].peek(k, now) for name, k in keys):
            return False                                  # check ALL first: a rejected request must not use up any quota
        for name, k in keys:
            self.rules[name].record(k, now)
        return True

    def evict_idle(self, now):                            # memory bound: forget keys whose window is empty
        for rule in self.rules.values():
            if isinstance(rule, SlidingWindowLog):
                for k in [k for k, log in rule.logs.items() if not log or log[-1] <= now - rule.window]:
                    del rule.logs[k]
            else:
                for k in [k for k, s in rule.state.items() if s[0] + 2 * rule.window <= now]:
                    del rule.state[k]
# --- end ---

def _exact(events, limit, window):                        # brute: re-count the whole history for every request
    accepted, out = [], []
    for t in events:
        ok = sum(1 for a in accepted if t - window < a <= t) < limit
        if ok:
            accepted.append(t)
        out.append(ok)
    return out

if __name__ == "__main__":
    rl = RateLimiter({"ip": (2, 10)})
    assert [rl.allow({"ip": "1.1.1.1"}, t) for t in (0, 1, 2, 9, 10, 11)] == [True, True, False, False, True, True]
    both = RateLimiter({"ip": (5, 10), "user": (2, 10)})  # user limit is the tight one
    assert [both.allow({"ip": "x", "user": "u"}, t) for t in (0, 1, 2)] == [True, True, False]
    assert len(both.rules["ip"].logs["x"]) == 2              # the rejected third request left no trace in the ip log
    assert both.allow({"ip": "y", "user": "u2"}, 3) is True      # a different user on the same IP-limit budget still passes
    rl.evict_idle(100)
    assert rl.rules["ip"].logs == {}
    rng = Random(2026)
    for _ in range(400):
        limit, window = rng.randint(1, 4), rng.randint(1, 6)
        ts = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 25)))
        rl = RateLimiter({"ip": (limit, window)})
        assert [rl.allow({"ip": "k"}, t) for t in ts] == _exact(ts, limit, window), (limit, window, ts)
        assert all(len(v) <= limit for v in rl.rules["ip"].logs.values())          # memory is bounded by the limit
    c = RateLimiter({"ip": (4, 10)}, SlidingWindowCounter)   # counter: prev * (1 - frac) + cur, hand-computed
    assert [c.allow({"ip": "k"}, t) for t in (0, 1, 2, 3)] == [True] * 4
    assert c.allow({"ip": "k"}, 10) is False             # prev=4 at frac 0 => estimate 4 >= limit
    assert c.allow({"ip": "k"}, 15) is True              # estimate 4 * 0.5 + 0 = 2 < 4
    for _ in range(300):                                  # the estimate never lets more than 'limit' through per bucket
        limit, window = rng.randint(1, 5), rng.randint(2, 8)
        c = RateLimiter({"ip": (limit, window)}, SlidingWindowCounter)
        per_bucket = {}
        for t in sorted(rng.randint(0, 40) for _ in range(30)):
            if c.allow({"ip": "k"}, t):
                per_bucket[t // window] = per_bucket.get(t // window, 0) + 1
        assert all(v <= limit for v in per_bucket.values()), (limit, window, per_bucket)
    print("OK amz_rate_limiter")
