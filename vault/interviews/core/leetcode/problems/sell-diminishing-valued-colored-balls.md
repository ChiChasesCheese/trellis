---
slug: sell-diminishing-valued-colored-balls
---
## Q
**LC 1648 销售价值减少的颜色球**｜Medium

库存里有若干种颜色的球，`inventory[i]` 是第 `i` 种颜色一开始的个数。顾客想买**任意颜色**、总数为 `orders` 的球。每个球的价值是它被卖出**那一刻**剩下的同色球个数（`6` 个黄球时卖出第一个价值 `6`，下一个价值 `5`，依此类推）。可以按任意顺序卖，返回卖出 `orders` 个球后能得到的**最大总价值**，对 `10^9 + 7` 取余。`1 <= inventory.length <= 10^5`，`1 <= inventory[i] <= 10^9`，`1 <= orders <= min(sum(inventory[i]), 10^9)`。例：`inventory = [2,5]`, `orders = 4` → `14`（`2 + 5 + 4 + 3`）；`inventory = [3,5]`, `orders = 6` → `19`；`inventory = [2,8,4,10,6]`, `orders = 20` → `110`；`inventory = [1000000000]`, `orders = 1000000000` → `21`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 贪心（先卖价值最高的球）+ 按"高度"分层 + 等差数列求和；订单量到 `10^9`，不能一个一个模拟。

**一句话。** 每次都卖当前价值最高的球；等价于把库存最高的几种颜色从上往下"削平"，一层一层卖，整层用等差数列求和，最后一层只卖一部分。

**识别。** 「价值随卖出递减」「每次选当前最大」= 贪心；`orders` 高达 `10^9`，用堆逐个模拟是 `O(orders log n)`，必须按块计算；答案取模、金额超 32 位，提示用等差数列公式。

**推导。** 价值最高的球永远应该先卖（拿走一个当前最大的，剩下的子问题价值不变），所以卖出的球一定是"价值从高到低"的前 `orders` 个。把库存降序排列后，最高的那种颜色先从 `inv[0]` 卖到 `inv[1]`，这一段只有一种颜色；此后前两种颜色并排，一起从 `inv[1]` 卖到 `inv[2]`……第 `i` 层有 `i + 1` 种颜色同时卖，层高 `inv[i] - inv[i+1]`。订单够卖完整层就整层累加；不够时，设还剩 `orders` 个、当前 `width` 种颜色，则每种先卖 `full = orders // width` 个，再有 `rest = orders % width` 种颜色多卖一个。

```python
def max_profit(inventory: list[int], orders: int) -> int:
    MOD = 10**9 + 7
    inv = sorted(inventory, reverse=True) + [0]  # 末尾补 0：最后一层一直卖到价值 1
    total = 0
    for i in range(len(inv) - 1):
        width = i + 1  # 前 i+1 种颜色此刻都已削到同一高度 inv[i]
        cur, nxt = inv[i], inv[i + 1]
        layer = width * (cur - nxt)  # 这些颜色一起从 cur 卖到 nxt，一共多少个球
        if orders >= layer:
            total += width * (cur + nxt + 1) * (cur - nxt) // 2  # 每种颜色的价值 nxt+1 .. cur，等差数列求和
            orders -= layer
        else:
            full, rest = divmod(orders, width)  # 每种颜色先卖 full 个，其中 rest 种再多卖 1 个
            total += width * (cur + cur - full + 1) * full // 2  # 每种卖 full 个：价值 cur .. cur-full+1
            total += rest * (cur - full)  # 多卖的那一个，价值 cur - full
            orders = 0
        if orders == 0:
            break
    return total % MOD  # Python 整数不溢出，最后统一取模
```

运行：四个示例依次得到 `14`、`19`、`110`、`21`；`([5], 1)` → `5`；`([1,1,1], 3)` → `3`。

**复杂度。** 时间 `O(n log n)`（排序），空间 `O(n)`。

**拓展优化。**
- 不排序全部：二分"价值阈值" `t`，使得把所有价值大于 `t` 的球卖掉的个数 `sold(t) <= orders` 的最小 `t`，剩下的订单都按价值 `t` 卖，`O(n log max)`，每轮 `O(n)`：

```python
def max_profit_threshold(inventory: list[int], orders: int) -> int:
    MOD = 10**9 + 7

    def sold(t: int) -> int:  # 卖掉所有价值 > t 的球的个数
        return sum(x - t for x in inventory if x > t)

    lo, hi = 0, max(inventory)  # 最小的 t 使得 sold(t) <= orders
    while lo < hi:
        mid = (lo + hi) // 2
        if sold(mid) <= orders:
            hi = mid
        else:
            lo = mid + 1
    t = lo
    total = sum((x + t + 1) * (x - t) // 2 for x in inventory if x > t)  # 价值 t+1 .. x 的球全卖
    total += (orders - sold(t)) * t  # 剩余订单都卖价值恰为 t 的球
    return total % MOD
```

**易错点。**
- 漏掉最后一层"多卖一个"的 `rest * (cur - full)`：`[2,5]`, `orders = 4` 得到 `12`，正确是 `14`。
- 用堆一个一个模拟：`inventory = [10^9]`, `orders = 10^9` 要循环 `10^9` 次，超时；必须按层用公式。
- 等差数列求和先对因子取模再除以 `2`：除法与取模不能随意交换，要么先算完整数值再取模（Python），要么用模逆元（Java / C++ 用 `long` 时要小心溢出）。

**追问。**
- 订单量很小（如 `orders <= 10^6`）：最大堆逐个卖，`O(orders log n)`，更直观，也是验证按层公式的暴力对拍。
- 要输出每种颜色卖了几个：用阈值版本得到 `t`，每种卖 `max(0, x - t)` 个，剩下的 `orders - sold(t)` 个各卖一个价值恰为 `t` 的球，分给任意库存 `>= t` 的颜色；因为 `t` 最小，剩余个数一定少于这样的颜色数。
- 为什么排序版第 `i` 层颜色数是 `i + 1`：降序后前 `i + 1` 种颜色此刻都已削到同一高度 `inv[i]`，更矮的颜色还没开始卖。

**同模式。** LC 1642 可以到达的最远建筑、LC 2208 将数组和减半的最少操作次数、LC 1005 K 次取反后最大化的数组和、LC 1167 连接木棍的最低费用。
