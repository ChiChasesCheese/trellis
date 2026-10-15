"""LC 871 Minimum Number of Refueling Stops -- drive until empty, then retroactively take the biggest passed station."""
import heapq
from itertools import combinations
from random import Random

# --- solution ---
def min_refuel_stops(target, start_fuel, stations):
    heap = []                                    # max-heap (negated) of fuel at stations we already drove past
    stops, i = 0, 0
    reach = start_fuel                           # farthest position we can reach with the fuel we have taken so far
    while reach < target:
        while i < len(stations) and stations[i][0] <= reach:
            heapq.heappush(heap, -stations[i][1])    # we COULD have stopped here: remember it
            i += 1
        if not heap:
            return -1                            # stuck: nothing passed can extend the range
        reach += -heapq.heappop(heap)            # greedy: the largest tank gives the farthest range
        stops += 1
    return stops
# --- end ---

def _brute(target, start_fuel, stations):
    for k in range(len(stations) + 1):
        for chosen in combinations(stations, k):          # stations are sorted by position, so is `chosen`
            fuel, pos, ok = start_fuel, 0, True
            for p, f in chosen:
                fuel -= p - pos
                if fuel < 0:
                    ok = False
                    break
                fuel += f
                pos = p
            if ok and fuel >= target - pos:
                return k
    return -1

if __name__ == "__main__":
    assert min_refuel_stops(1, 1, []) == 0
    assert min_refuel_stops(100, 1, [[10, 100]]) == -1
    assert min_refuel_stops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]) == 2
    assert min_refuel_stops(100, 50, [[25, 25], [50, 50]]) == 1
    rng = Random(8)
    for _ in range(600):
        target = rng.randint(1, 30)
        pos = sorted(rng.sample(range(1, 30), rng.randint(0, 6)))
        pos = [p for p in pos if p < target]
        stations = [[p, rng.randint(1, 15)] for p in pos]
        sf = rng.randint(1, 15)
        assert min_refuel_stops(target, sf, stations) == _brute(target, sf, [tuple(s) for s in stations]), (target, sf, stations)
    print("ok 871_minimum_number_of_refueling_stops")
