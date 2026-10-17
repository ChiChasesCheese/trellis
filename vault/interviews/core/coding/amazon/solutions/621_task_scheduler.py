"""LC 621 Task Scheduler -- count the most frequent task, fill the idle gaps (closed form). O(n + 26)."""
from collections import Counter, deque
from random import Random
import heapq

# --- solution ---
def least_interval(tasks, n):
    counts = Counter(tasks).values()
    top = max(counts)                                    # the busiest task fixes the frame count
    how_many_top = sum(1 for c in counts if c == top)    # tasks tied for busiest share the last frame
    frames_len = (top - 1) * (n + 1) + how_many_top      # (top-1) full frames of n+1 slots, then the tail
    return max(len(tasks), frames_len)                   # if there are plenty of tasks, no idle is needed


def least_interval_simulated(tasks, n):                  # the same answer by running the schedule (max-heap + cooldown queue)
    heap = [-c for c in Counter(tasks).values()]
    heapq.heapify(heap)
    cooling = deque()                                    # (time_ready, remaining_count)
    time = 0
    while heap or cooling:
        time += 1
        if heap:
            left = -heapq.heappop(heap) - 1              # run the task with the most work left
            if left:
                cooling.append((time + n, left))
        if cooling and cooling[0][0] == time:            # cooldown over: eligible again
            heapq.heappush(heap, -cooling.popleft()[1])
    return time
# --- end ---

def _brute(tasks, n):
    """Exhaustive BFS over (remaining counts, last-run times): minimum number of slots, idle allowed."""
    names = sorted(set(tasks))
    frontier = {(tuple(tasks.count(t) for t in names), (-10 ** 9,) * len(names))}
    t = 0
    while True:
        nxt = set()
        for counts, last in frontier:
            if not any(counts):
                return t
            moves = [None] + [i for i in range(len(names)) if counts[i] and t - last[i] > n]
            for m in moves:
                c, l = list(counts), list(last)
                if m is not None:
                    c[m] -= 1
                    l[m] = t
                nxt.add((tuple(c), tuple(l)))
        frontier, t = nxt, t + 1

if __name__ == "__main__":
    assert least_interval(list("AAABBB"), 2) == 8
    assert least_interval(list("AAABBB"), 0) == 6
    assert least_interval(list("AAAAAABCDEFG"), 2) == 16
    assert least_interval(list("A"), 100) == 1
    assert least_interval(list("ABCABCDDD"), 3) == 9
    rng = Random(9)
    for _ in range(150):
        tasks = [rng.choice("ABCD") for _ in range(rng.randint(1, 7))]
        n = rng.randint(0, 3)
        want = _brute(tasks, n)
        assert least_interval(tasks, n) == want, (tasks, n)
        assert least_interval_simulated(tasks, n) == want, (tasks, n)
    print("ok 621_task_scheduler")
