"""LC 347 Top K Frequent Elements -- Counter + size-k min-heap. Time O(n log k), space O(n)."""
import heapq
from collections import Counter

# --- solution ---
def top_k_frequent(nums, k):
    freq = Counter(nums)
    heap = []                                   # min-heap of (count, value), never more than k items
    for value, count in freq.items():
        heapq.heappush(heap, (count, value))
        if len(heap) > k:
            heapq.heappop(heap)                 # evict the least frequent of the k+1
    return [value for _, value in heap]


def top_k_frequent_buckets(nums, k):
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]   # buckets[c] = values that appear c times
    for value, count in freq.items():
        buckets[count].append(value)
    out = []
    for count in range(len(nums), 0, -1):
        for value in buckets[count]:
            out.append(value)
            if len(out) == k:
                return out
    return out
# --- end ---

if __name__ == "__main__":
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    assert sorted(top_k_frequent([4, 4, 4, 5, 5, 6, 7, 7, 7, 7], 2)) == [4, 7]
    assert sorted(top_k_frequent_buckets([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert sorted(top_k_frequent_buckets([-1, -1], 1)) == [-1]
    print("ok 347_top_k_frequent_elements")
