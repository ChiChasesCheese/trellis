---
id: tlc-python-recursion-memo-2-top-down-bottom-up
node: python.recursion-memo
type: qa
step: 2
---
## Q
**Python 递归｜记忆化搜索改成自底向上递推**

零钱兑换（LC 322）的记忆化版本为什么在 `amount` 很大时会爆栈？怎样机械地把它改写成递推，改写要保证什么？

## A
```python
from functools import cache
def coin_change_td(coins: list[int], amount: int) -> int:
    inf = float("inf")
    @cache
    def f(r: int) -> float:
        if r == 0: return 0
        if r < 0: return inf
        return 1 + min((f(r - c) for c in coins), default=inf)
    ans = f(amount)
    return -1 if ans == inf else int(ans)
def coin_change_bu(coins: list[int], amount: int) -> int:
    inf = float("inf")
    dp = [0] + [inf] * amount
    for r in range(1, amount + 1):          # 从小到大：f(r) 依赖更小的 r，已经算好
        for c in coins:
            if c <= r and dp[r - c] + 1 < dp[r]:
                dp[r] = dp[r - c] + 1
    return -1 if dp[amount] == inf else dp[amount]
print(coin_change_td([1, 2, 5], 11), coin_change_bu([1, 2, 5], 11))   # 3 3
print(coin_change_td([2], 3), coin_change_bu([2], 3))                  # -1 -1
print(coin_change_bu([1], 20000))                                      # 20000
```

- `coin_change_td([1], 5000)` 递归深度 `5000`，默认上限 `1000` 下会抛 `RecursionError`；`bu` 版只有一层循环，不受影响。
- 改写步骤：① 写出状态（这里 `r`）；② 看递归调用的方向（`r` 依赖 `r - c`，即更小的值）；③ 按**依赖在先**的顺序循环；④ 递归的 base case 变成数组初值。
- 依赖方向决定循环方向：依赖更小的 → 从小到大；依赖更大的（区间 DP）→ 按区间长度从短到长。
- 自底向上可以进一步滚动数组压缩空间；记忆化不能。
- 面试策略：先写记忆化把答案写对，再说「这个深度会爆栈，可以改自底向上」，需要时再改。
