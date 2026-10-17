"""LC 767 Reorganize String -- max-heap on counts, hold back the char just used. Time O(n log a), a = alphabet."""
import heapq
from collections import Counter

# --- solution ---
def reorganize_string(s):
    heap = [(-c, ch) for ch, c in Counter(s).items()]      # max-heap via negated counts
    heapq.heapify(heap)
    out = []
    held = None                                            # (neg_count, ch) used last step, not yet reusable
    while heap or held:
        if not heap:                                       # only the held char is left -> would be adjacent
            return ""
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        if held:
            heapq.heappush(heap, held)                     # now it's no longer adjacent to itself
            held = None
        if neg + 1 < 0:                                    # still has copies left
            held = (neg + 1, ch)
    return "".join(out)
# --- end ---

def _valid(src, res):
    return (sorted(res) == sorted(src)
            and all(res[i] != res[i + 1] for i in range(len(res) - 1)))

if __name__ == "__main__":
    assert _valid("aab", reorganize_string("aab"))
    assert reorganize_string("aaab") == ""
    assert reorganize_string("a") == "a"
    assert _valid("aabbcc", reorganize_string("aabbcc"))
    assert _valid("vvvlo", reorganize_string("vvvlo"))
    assert _valid("aaaabbc", reorganize_string("aaaabbc"))   # 4 a's in 7 slots: exactly a?a?a?a
    assert reorganize_string("aaaaabbc") == ""               # 5 a's in 8 slots: impossible
    print("ok 767_reorganize_string")
