"""LC 332 Reconstruct Itinerary -- Hierholzer's Eulerian path, iterative; smallest-lexical edge first, answer built in reverse."""
from random import Random

# --- solution ---
def find_itinerary(tickets):
    graph = {}
    for a, b in sorted(tickets, reverse=True):            # reverse-sorted so pop() yields the smallest destination
        graph.setdefault(a, []).append(b)
    stack, route = ["JFK"], []
    while stack:
        while graph.get(stack[-1]):                       # walk until stuck (this is the dead end)
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())                         # a stuck airport is the LAST of what remains
    return route[::-1]
# --- end ---

def _brute(tickets):
    ts = sorted(tickets)
    used = [False] * len(ts)
    def go(cur, path):
        if len(path) == len(ts) + 1:
            return path
        for i, (a, b) in enumerate(ts):
            if not used[i] and a == cur:
                used[i] = True
                got = go(b, path + [b])
                if got:
                    return got
                used[i] = False
        return None
    return go("JFK", ["JFK"])

if __name__ == "__main__":
    assert find_itinerary([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]) == ["JFK", "MUC", "LHR", "SFO", "SJC"]
    assert find_itinerary([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]) == ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]
    rng = Random(332)
    names = ["JFK", "AAA", "BBB", "CCC", "DDD"]
    for _ in range(500):
        cur, tickets = "JFK", []
        for _ in range(rng.randint(1, 8)):                # random walk from JFK => an Eulerian path is guaranteed
            nxt = rng.choice([x for x in names if x != cur])
            tickets.append([cur, nxt])
            cur = nxt
        assert find_itinerary(tickets) == _brute(tickets), tickets
    chain = [["JFK", "A"]] + [["A", "B"], ["B", "A"]] * 150      # 301 tickets, long path, no recursion limit hit
    assert len(find_itinerary(chain[:1] + [["A", "B"], ["B", "A"]] * 149 + [["A", "Z"]])) == 301
    print("ok 332_reconstruct_itinerary")
