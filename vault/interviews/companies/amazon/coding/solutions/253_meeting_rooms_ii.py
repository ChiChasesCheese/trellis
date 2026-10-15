"""LC 253 Meeting Rooms II -- sweep over sorted starts/ends (or a heap of end times). Time O(n log n)."""
import heapq
from random import Random

# --- solution ---
def min_meeting_rooms(intervals):
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = best = 0
    j = 0                                   # next meeting to end
    for s in starts:
        while ends[j] <= s:                 # a meeting ending exactly at s frees its room first
            j += 1
            rooms -= 1
        rooms += 1
        best = max(best, rooms)
    return best


def min_meeting_rooms_heap(intervals):
    heap = []                               # end times of rooms currently in use
    for s, e in sorted(intervals):
        if heap and heap[0] <= s:           # earliest-finishing room is free: reuse it
            heapq.heapreplace(heap, e)
        else:
            heapq.heappush(heap, e)         # need a new room
    return len(heap)
# --- end ---

def _brute(iv):
    pts = sorted({t for s, e in iv for t in (s, e)})
    return max((sum(1 for s, e in iv if s <= t < e) for t in pts), default=0)

if __name__ == "__main__":
    for f in (min_meeting_rooms, min_meeting_rooms_heap):
        assert f([[0, 30], [5, 10], [15, 20]]) == 2
        assert f([[7, 10], [2, 4]]) == 1
        assert f([[1, 5], [5, 8]]) == 1                   # back-to-back reuses the room
        assert f([[1, 5], [1, 5], [1, 5]]) == 3
        assert f([]) == 0
        rng = Random(5)
        for _ in range(300):
            iv = []
            for _ in range(rng.randint(0, 7)):
                a = rng.randint(0, 8)
                iv.append([a, a + rng.randint(1, 4)])
            assert f(iv) == _brute(iv), iv
    print("ok 253_meeting_rooms_ii")
