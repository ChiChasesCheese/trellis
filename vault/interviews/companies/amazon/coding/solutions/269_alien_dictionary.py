"""LC 269 Alien Dictionary -- derive letter edges from adjacent words, then topological sort. Time O(total chars)."""
from collections import deque

# --- solution ---
def alien_order(words):
    graph = {ch: set() for w in words for ch in w}        # every letter is a node, even with no edges
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                graph[x].add(y)                           # first difference decides: x < y
                break
        else:
            if len(a) > len(b):                           # "abc" before "ab" is impossible
                return ""
    indegree = {ch: 0 for ch in graph}
    for ch in graph:
        for nxt in graph[ch]:
            indegree[nxt] += 1
    queue = deque(ch for ch in graph if indegree[ch] == 0)
    out = []
    while queue:
        ch = queue.popleft()
        out.append(ch)
        for nxt in graph[ch]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return "".join(out) if len(out) == len(graph) else ""   # cycle -> no valid order
# --- end ---

if __name__ == "__main__":
    order = alien_order(["wrt", "wrf", "er", "ett", "rftt"])
    assert order == "wertf"
    assert alien_order(["z", "x"]) == "zx"
    assert alien_order(["z", "x", "z"]) == ""            # cycle
    assert alien_order(["abc", "ab"]) == ""              # prefix rule violated
    assert sorted(alien_order(["z", "z"])) == ["z"]
    print("ok 269_alien_dictionary")
