"""LC 815 Bus Routes -- BFS where a node is a ROUTE (boarding one bus = 1 ride); stop -> routes index makes it O(sum len)."""
from collections import deque
from random import Random

# --- solution ---
def num_buses_to_destination(routes, source, target):
    if source == target:
        return 0
    stop_to_routes = {}
    for i, route in enumerate(routes):
        for stop in route:
            stop_to_routes.setdefault(stop, []).append(i)
    queue = deque((r, 1) for r in stop_to_routes.get(source, []))
    seen_routes = {r for r, _ in queue}
    seen_stops = {source}
    while queue:
        r, rides = queue.popleft()
        for stop in routes[r]:
            if stop == target:
                return rides
            if stop in seen_stops:                        # every route through this stop was queued already
                continue
            seen_stops.add(stop)
            for nxt in stop_to_routes[stop]:
                if nxt not in seen_routes:
                    seen_routes.add(nxt)
                    queue.append((nxt, rides + 1))
    return -1
# --- end ---

def _brute(routes, source, target):
    reach, rides = {source}, 0                            # stops reachable with exactly <= rides buses
    while True:
        if target in reach:
            return rides
        bigger = set(reach)
        for route in routes:
            if reach & set(route):
                bigger |= set(route)
        if bigger == reach:
            return -1
        reach, rides = bigger, rides + 1

if __name__ == "__main__":
    assert num_buses_to_destination([[1, 2, 7], [3, 6, 7]], 1, 6) == 2
    assert num_buses_to_destination([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12) == -1
    assert num_buses_to_destination([[1, 2]], 5, 5) == 0
    rng = Random(815)
    for _ in range(500):
        routes = [rng.sample(range(10), rng.randint(1, 4)) for _ in range(rng.randint(1, 6))]
        s, t = rng.randrange(12), rng.randrange(12)
        assert num_buses_to_destination(routes, s, t) == _brute(routes, s, t), (routes, s, t)
    print("ok 815_bus_routes")
