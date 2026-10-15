"""LC 121 Best Time to Buy and Sell Stock -- track the cheapest price so far. Time O(n), space O(1)."""
from random import Random

# --- solution ---
def max_profit(prices):
    cheapest = float("inf")
    best = 0
    for p in prices:
        cheapest = min(cheapest, p)          # best day to have bought, among days up to today
        best = max(best, p - cheapest)       # sell today
    return best
# --- end ---

def _brute(p):
    return max([0] + [p[j] - p[i] for i in range(len(p)) for j in range(i + 1, len(p))])

if __name__ == "__main__":
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit([7, 6, 4, 3, 1]) == 0          # only goes down: don't trade
    assert max_profit([]) == 0
    assert max_profit([5]) == 0
    assert max_profit([2, 4, 1]) == 2
    rng = Random(16)
    for _ in range(300):
        p = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
        assert max_profit(p) == _brute(p), p
    print("ok 121_best_time_to_buy_and_sell_stock")
