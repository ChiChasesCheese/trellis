"""LC 295 Find Median from Data Stream -- two heaps (max-heap low half, min-heap high half). add O(log n), median O(1)."""
import heapq
from random import Random

# --- solution ---
class MedianFinder:
    def __init__(self):
        self.low = []     # max-heap (store negatives): the smaller half
        self.high = []    # min-heap: the larger half; invariant len(low) in {len(high), len(high)+1}

    def add_num(self, num):
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))   # push through low so ordering low <= high holds
        if len(self.high) > len(self.low):                    # rebalance: low may hold one extra
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def find_median(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
# --- end ---

if __name__ == "__main__":
    m = MedianFinder()
    m.add_num(1)
    m.add_num(2)
    assert m.find_median() == 1.5
    m.add_num(3)
    assert m.find_median() == 2.0
    rng = Random(11)
    for _ in range(100):
        m, seen = MedianFinder(), []
        for _ in range(rng.randint(1, 15)):
            x = rng.randint(-10, 10)
            m.add_num(x)
            seen.append(x)
            s = sorted(seen)
            n = len(s)
            want = float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
            assert m.find_median() == want, (seen,)
    print("ok 295_find_median_from_data_stream")
