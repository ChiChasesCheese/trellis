"""LC 134 Gas Station -- one pass: if the tank dies at i, no start in [start, i] works. Time O(n), space O(1)."""
from random import Random

# --- solution ---
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1                              # not enough fuel in total: impossible from anywhere
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                           # stuck at i: every start in [start, i] would be stuck too
            start, tank = i + 1, 0
    return start                               # the total is >= 0, so the last surviving candidate works
# --- end ---

def _ok(gas, cost, s):
    n, tank = len(gas), 0
    for k in range(n):
        i = (s + k) % n
        tank += gas[i] - cost[i]
        if tank < 0:
            return False
    return True

def _brute(gas, cost):
    for s in range(len(gas)):
        if _ok(gas, cost, s):
            return s
    return -1

if __name__ == "__main__":
    assert can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
    assert can_complete_circuit([5], [4]) == 0
    assert can_complete_circuit([3], [4]) == -1
    rng = Random(2)
    for _ in range(1000):
        n = rng.randint(1, 8)
        gas = [rng.randint(0, 6) for _ in range(n)]
        cost = [rng.randint(0, 6) for _ in range(n)]
        got, want = can_complete_circuit(gas, cost), _brute(gas, cost)
        assert (got == -1) == (want == -1), (gas, cost)
        if got != -1:
            assert _ok(gas, cost, got), (gas, cost, got)       # any valid start is acceptable (LeetCode guarantees uniqueness; random data may not)
    print("ok 134_gas_station")
