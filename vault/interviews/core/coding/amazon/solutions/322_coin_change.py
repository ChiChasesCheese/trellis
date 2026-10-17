"""LC 322 Coin Change -- dp[a] = 1 + min(dp[a - c]). Time O(amount * coins), space O(amount)."""
from random import Random

# --- solution ---
def coin_change(coins, amount):
    INF = amount + 1                       # larger than any real answer
    dp = [0] + [INF] * amount              # dp[a] = fewest coins to make a
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
# --- end ---

def _brute(coins, amount):
    best = [None]
    def go(rem, used):
        if rem == 0:
            best[0] = used if best[0] is None else min(best[0], used)
            return
        for c in coins:
            if c <= rem and (best[0] is None or used + 1 < best[0]):
                go(rem - c, used + 1)
    go(amount, 0)
    return -1 if best[0] is None else best[0]

if __name__ == "__main__":
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    assert coin_change([186, 419, 83, 408], 6249) == 20          # greedy would fail; DP is fine
    assert coin_change([2, 5, 10, 1], 27) == 4
    rng = Random(18)
    for _ in range(150):
        cs = rng.sample(range(1, 8), rng.randint(1, 3))
        amt = rng.randint(0, 20)
        assert coin_change(cs, amt) == _brute(cs, amt), (cs, amt)
    print("ok 322_coin_change")
