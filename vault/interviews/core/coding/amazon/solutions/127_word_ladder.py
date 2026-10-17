"""LC 127 Word Ladder -- BFS over words, neighbours via wildcard buckets (h*t). Time O(N * L^2), space O(N * L^2)."""
from collections import defaultdict, deque

# --- solution ---
def ladder_length(begin, end, word_list):
    if end not in set(word_list):
        return 0
    buckets = defaultdict(list)                       # "h*t" -> ["hot", "hit", ...]
    for w in set(word_list) | {begin}:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    queue = deque([(begin, 1)])
    seen = {begin}
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            key = word[:i] + "*" + word[i + 1:]
            for nxt in buckets.pop(key, []):          # pop: each bucket is expanded only once
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return 0
# --- end ---

if __name__ == "__main__":
    wl = ["hot", "dot", "dog", "lot", "log", "cog"]
    assert ladder_length("hit", "cog", wl) == 5
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0     # end not in list
    assert ladder_length("a", "c", ["a", "b", "c"]) == 2
    assert ladder_length("hit", "hit", ["hit"]) == 1
    print("ok 127_word_ladder")
