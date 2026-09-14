# pc23 · Min Coins with Change：练的是"贪心失效就换 DP，证不出上界就用测试兜底"

> [!tldr]
> - 这题考的是：付款 + 找零的硬币总数最小化，从固定 canonical 面额到任意面额（戳破贪心）再到构造具体拆法；三段规则均超出预览，**(reconstructed)**
> - 三步套路：无界零钱兑换 DP 算 `min_coins(x)` → 在 `[n, n+window]` 里搜索付款金额，取 `dp[付款]+dp[找零]` 最小值 → DP 表回溯出具体的付款/找零硬币
> - 最值得带走的一个模式：**面额集合不保证 canonical 时贪心可能不是最优解，一律换成 DP；证不出严格上界就用经验验证 + 更宽窗口的回归测试兜底，诚实说明证明的边界**

## 1. 题目在说什么（人话版）

欠 `n` 元，可以多付一些钱 `P >= n`（用固定面额组成），收银台用同一套面额找零 `C = P - n`，
目标是让"付出的硬币数 + 找回的硬币数"之和最小——不是只求付款的最少硬币数。

小例子：
```
min_total_coins_fixed(4) = 2      # 付 5，找 1
min_total_coins_fixed(6) = 2      # 付 5+1 恰好，0 找零
min_total_coins_custom(6, [1,3,4]) = 2   # 3+3；贪心会先取 4 再两个 1，给出 3 枚
```

## 2. 读题：把文字变成模型

- **实体**：面额集合、付款金额、找零金额。
- **输入**：`n`（Part 2/3 还有 `denominations`）。
- **输出**：最小硬币总数（Part 3 是具体的付款/找零硬币列表）。
- **状态**：一个按面额缓存的 DP 数组，随查询按需扩展。
- **一句话建模**：这是一个 **"双向零钱兑换"** 问题——付款和找零两侧都要用同一套 DP，答案是
  在一个有限窗口里搜索付款金额，取两侧 DP 值之和的最小值。

> [!note] 为什么不能用贪心
> 贪心只在"canonical"面额集合上最优。Part 2 故意给出反例 `{1,3,4}`：凑 6，贪心先取 4 再取
> 两个 1，共 3 枚；DP 给出 `3+3`，共 2 枚。判断一个集合是否 canonical 本身不平凡，面试里不需要
> 展开，只需要知道"不确定就用 DP"。

## 3. 下笔顺序

1. **问清**：面额集合是否保证包含 1？是否保证能凑出任意金额？
2. **Part 1 最小可用**：标准无界零钱兑换 DP，`dp[x] = min(dp[x-d]+1 for d in denoms)`；在
   `P ∈ [n, n+window]` 里搜索 `dp[P] + dp[P-n]` 的最小值，`window = max(denoms)`。
3. **Part 2 叠加**：换成任意面额集合，窗口翻倍到 `2*max(denoms)` 留余量，DP 核心完全复用。
4. **Part 3 叠加**：复用同一个 DP 表，回溯时按"面额从大到小"确定性地拆出付款和找零两侧的具体
   硬币。
5. **收尾**：面额集合无法凑出目标金额要 `ValueError`；`n=0` 两侧都是空列表；用一个 checker
   （验证面额合法 + 净额正确 + 总数最优）而不是逐字符比对来验证 Part 3，因为最优拆法可能不唯一。

## 4. 代码怎么组织

```
_get_dp(denominations, size) -> dp[]          # 按需扩展的缓存 DP 数组，三个 Part 共用
min_coins(x, denoms)                          # 单侧最小硬币数
_min_total(n, denoms, multiplier)             # 付款+找零双向搜索，Part 1/2 共用
min_total_coins_fixed / min_total_coins_custom
min_total_coins_breakdown(n, denoms)          # Part 3：复用 DP 表 + 回溯
is_valid_optimal_breakdown(...)               # 测试用 checker，不逐字符比对
```
Part 1 和 Part 2 除了窗口倍数（1x vs 2x）和面额是否固定，其余逻辑完全共享 `_min_total`。

## 5. 核心代码（骨架）

```python
CANONICAL = (1, 5, 10, 50, 100, 200)
INF = float("inf")

def _get_dp(denoms, size):
    dp = [0] + [INF] * size
    for x in range(1, size + 1):
        dp[x] = min((dp[x - d] + 1 for d in denoms if d <= x), default=INF)
    return dp

def _min_total(n, denoms, multiplier):
    window = multiplier * max(denoms)
    dp = _get_dp(denoms, n + window)
    best = INF
    for w in range(window + 1):
        paid = n + w
        if dp[paid] != INF and dp[w] != INF:
            best = min(best, dp[paid] + dp[w])
    if best == INF:
        raise ValueError(f"{n} is unreachable with denominations {denoms}")
    return best

def min_total_coins_fixed(n):
    return _min_total(n, CANONICAL, multiplier=1)

def min_total_coins_custom(n, denominations):
    denoms = tuple(sorted(set(denominations)))
    return _min_total(n, denoms, multiplier=2)   # 非熟悉集合，窗口翻倍留余量
```

## 6. 面试里怎么说

- 开始前：「面额集合保证包含 1 吗？如果不保证，有些金额可能凑不出来，我需要报错。」
- 写 Part 1 时：「我用无界零钱兑换 DP，不用贪心——虽然固定面额恰好是 canonical，贪心对它是对
  的，但我想让 Part 1/2 共用同一份 DP 核心。真正要付的金额理论上无上界，但我把搜索窗口限制在
  `[n, n+max(denoms)]`，因为经验上更宽的窗口不会改变答案。」
- 到搜索上界被追问时：「`dp` 对 x 并不单调，我证不出一个对任意面额集合都成立的紧上界，所以我
  用经验验证 + 更宽窗口的回归测试兜底，而不是假装有一个严格证明。」
- 交付时：「样例过了；Part 3 的具体拆法可能不唯一，我用 checker 验证总数最优而不是逐字符比对。」

## 7. 常见跑偏

- Part 2 直接套贪心（面额从大到小尽量取），被 `{1,3,4}` 凑 6 的例子戳穿。
- 只算付款一侧的最少硬币数，忘了"付款+找零"是两侧都要 DP 的组合优化。
- 搜索窗口设得太小（比如只搜 `[n, n]`，即恰好付出 n），漏掉"多付再找零"反而更优的情况。

## 8. 同族题 / 延伸

- 与 `q06`（Patching Array）同属"贪心 vs 构造性验证"的考法，但 pc23 是背包型 DP，q06 是区间
  覆盖贪心。
- 与 `pc18`（Number Transformation Path）同样需要"论证一个有限的搜索上界"，但 pc18 靠奇偶性
  给出严格证明，pc23 只能靠经验验证 + 测试兜底，诚实说明证明的边界是这题的重点。
- 练习命令：`python3 loop/mock.py start pc23`

## 索引行

| [pc23_min_coins_with_change](pc23_min_coins_with_change.md) | `../../loop/rounds/03_phone_coding/pc23_min_coins_with_change/` | 电面 coding | 面额集合不保证 canonical 时贪心可能不是最优解，一律换成 DP；证不出严格上界就用经验验证 + 更宽窗口的回归测试兜底，诚实说明证明的边界 |
