"""LC 1235 Maximum Profit in Job Scheduling -- weighted interval scheduling: sort by end, DP + binary search. O(n log n)."""
import bisect
from itertools import combinations
from random import Random

# --- solution ---
def job_scheduling(start_time, end_time, profit):
    jobs = sorted(zip(end_time, start_time, profit))      # by end time
    ends = [e for e, _, _ in jobs]
    dp = [0] * (len(jobs) + 1)                            # dp[i]: best profit using the first i jobs
    for i, (e, s, p) in enumerate(jobs, 1):
        k = bisect.bisect_right(ends, s, 0, i - 1)        # jobs that end at or before s are compatible
        dp[i] = max(dp[i - 1], dp[k] + p)                 # skip job i, or take it on top of dp[k]
    return dp[-1]
# --- end ---

def _brute(st, en, pr):
    n = len(st)
    best = 0
    for r in range(n + 1):
        for comb in combinations(range(n), r):
            c = sorted(comb, key=lambda i: st[i])
            if all(en[c[i]] <= st[c[i + 1]] for i in range(len(c) - 1)):
                best = max(best, sum(pr[i] for i in c))
    return best

if __name__ == "__main__":
    assert job_scheduling([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
    assert job_scheduling([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]) == 150
    assert job_scheduling([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6
    assert job_scheduling([1], [2], [7]) == 7
    rng = Random(26)
    for _ in range(300):
        n = rng.randint(1, 7)
        st = [rng.randint(0, 8) for _ in range(n)]
        en = [s + rng.randint(1, 4) for s in st]
        pr = [rng.randint(1, 9) for _ in range(n)]
        assert job_scheduling(st, en, pr) == _brute(st, en, pr), (st, en, pr)
    print("ok 1235_maximum_profit_in_job_scheduling")
