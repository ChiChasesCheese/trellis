# pc23 · Min Coins with Change — 找零最小化的“付 + 找”双向 DP

> TrueInterview 87 题清单中的一手题面预览；三段规则均超出预览可见文字，**均标 (reconstructed)**。

## 背景

TrueInterview 同步的 Snowflake Algo 题单第 23 项：「Min Coins with Change」，付款面额固定为
`{1, 5, 10, 50, 100, 200}`（无限供应）。付款人可以多付，收银台用同一套面额找零，目标是让
**付出的硬币数 + 找回的硬币数**之和最小——不是只求付款的最少硬币数（那是纯粹的教科书零钱兑换）。

这题的坑是两层：① 付款金额本身要不要恰好等于 `n`，是一个需要搜索的自由变量；② 面额集合一旦不是
"canonical"（贪心即最优），必须换成 DP，Part 2 就是故意给一个非 canonical 集合戳破贪心。

## 输入

- Part 1：`n: int`，`0 <= n <= 10000`，面额固定为 `(1, 5, 10, 50, 100, 200)`。
- Part 2：`n: int`（同上范围）与 `denominations: list[int]`（正整数，去重后至少 1 个，不保证
  canonical，不保证包含 1——若某个金额在给定面额下无法凑出，`ValueError`）。
- Part 3：与 Part 1/2 相同的输入，返回一组具体的硬币构成而非只返回总数。

## API 契约（英文签名）

```python
def min_coins(x: int, denominations: tuple[int, ...] = CANONICAL_DENOMINATIONS) -> int
def min_total_coins_fixed(n: int) -> int
def min_total_coins_custom(n: int, denominations: list[int]) -> int
def min_total_coins_breakdown(n: int, denominations=CANONICAL_DENOMINATIONS) -> tuple[list[int], list[int]]
def is_valid_optimal_breakdown(n, paid, change, denominations=CANONICAL_DENOMINATIONS) -> bool
```

`n < 0` 或面额里出现非正数 → `ValueError`；给定面额无法凑出所需金额 → `ValueError`。

## 规则

### Part 1 — 固定面额，n up to 1e4

`min_coins(x)` 用标准无界零钱兑换 DP（**不是贪心**——虽然 `{1,5,10,50,100,200}` 恰好是
canonical 集合，贪心对它是对的，但 Part 2 会给出贪心失效的集合，所以两个 Part 共用同一个 DP
核心，只是 Part 1 传入固定面额）。

**搜索上界的证明/论证**：真正要付的金额 `P >= n` 理论上无上界，但只需要在
`P ∈ [n, n + max(denoms)]` 里搜索（即 `window = max(denoms) = 200`）：

- `dp(x)` 满足次可加性 `dp(a+b) <= dp(a) + dp(b)`（把 a、b 各自的最优分解拼起来即可），但 **`dp`
  对 `x` 并不单调**——`{1,5}` 下 `dp(4)=4 > dp(5)=1`——所以"付更多只会更贵"这种直觉式交换论证在
  一般面额集合下并不严格成立，写不出一个对任意面额集合都成立的紧上界证明。
- 退而求其次，**用计算验证**：对 `{1,5,10,50,100,200}`，把窗口从 `max(denoms)=200` 放大到
  `5*max(denoms)=1000`，在 `n = 0..10000` 全部整数上重新计算，答案 **零处不同**（见
  `test_pc23.py::test_window_bound_matches_wider_window`，随测试套件重新验证，而不是只信一次性
  脚本）。
- 因此 Part 1 的 `window = max(denoms)` 是"经验上界 + 测试兜底"，不是形式化证明；如果以后换一个
  病态面额集合，测试会先失败再暴露问题，而不是静默给错答案。

### Part 2 — 任意面额集合，贪心失效 **(reconstructed)**

给定 `denominations`（不保证 canonical，例如 `{1, 3, 4}`：凑 `6`，贪心先取 `4` 再取两个
`1`，共 3 枚；DP 给出 `3+3`，共 2 枚——贪心不是最优）。因此 Part 2 **必须用 DP**，付款和找零两
侧都要 DP。

上界论证同 Part 1，但因为面额集合不再是"熟悉的"canonical 集合，多留一倍余量：
`window = 2 * max(denoms)`。同样只是经验上界（`test_pc23.py` 对 `{1,3,4}` 在 `n=0..2000` 上把
`window` 和 `5*max(denoms)` 做了逐一比较，零处不同），不是形式证明。

### Part 3 — 返回一组具体的付款/找零硬币 **(reconstructed)**

`min_total_coins_breakdown(n, denominations)` 返回 `(paid_coins, change_coins)`：`paid_coins`
之和减 `change_coins` 之和等于 `n`，且 `len(paid_coins) + len(change_coins)` 等于该面额集合下的
最优总数。**最优分解不唯一**（比如恰好凑出 `n` 本身可能有多种付法达到同样总数时，只要满足总数
最优即可），所以测试用 `is_valid_optimal_breakdown` 这个 checker 验证任意实现返回的分解，而不是
逐字符比对；DP 回溯时按"面额从大到小尝试"做了确定性打破平局，方便写回归用的精确字符串测试。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**：`min_total_coins_fixed(0) = 0`（不用付也不用找）
**例 2**：`min_total_coins_fixed(4) = 2`（付 `5`，找 `1`）
**例 3**：`min_total_coins_fixed(6) = 2`（付 `5+1` 恰好，`0` 找零）
**例 4**：`min_total_coins_fixed(999) = 6`（付 `200*5=1000`，找 `1`）
**例 5**：`min_total_coins_fixed(10000) = 50`（付 `200*50` 恰好）
**例 6**：`min_total_coins_custom(6, [1,3,4]) = 2`（`3+3`；贪心会给 3）
**例 7**：`min_total_coins_custom(7, [1,3,4]) = 2`（`4+3` 恰好）
**例 8**：`min_total_coins_breakdown(4) = ([5], [1])`
**例 9**：`min_total_coins_breakdown(999) = ([200,200,200,200,200], [1])`
**例 10**：`min_total_coins_breakdown(6, [1,3,4]) = ([3,3], [])`

## `main()` 命令流

```
PART 1                    PART 2                        PART 3
N 4                       D 1 3 4                       D 1 3 4
0                         N 2                            N 2
4                         6                               6
6                         7                                0
999                       → 2                            → 3,3|-
→ 0                         2                               -|-
  2
  2
  6
```

```
PART 3
D 1 5 10 50 100 200
N 2
4
999
→ 5|1
  200,200,200,200,200|1
```

每行输出 `paid|change`，两侧各自是面额从大到小、逗号分隔的列表；空列表输出 `-`。

## 边界清单

- `n = 0`（不付不找，两侧都是 `-`）
- `n` 本身恰好可以精确凑出（找零为 `0`）
- Part 2 面额里没有 `1`，且给定的 `n` 无法用这些面额（也无法通过任何找零组合）凑出 → `ValueError`
- Part 2 面额含重复值 / 未排序（内部会去重排序）
- 负的 `n`、非正的面额 → `ValueError`
- Part 1 的 `n = 10000`（题目声明的上界）
- Part 3 最优分解不唯一时，checker 只验证"总数最优 + 面额合法 + 净额正确"，不比较具体拆法
- 找零窗口的经验上界必须被 `test_window_bound_matches_wider_window` 覆盖，而不是只靠人工肉眼检查

## 追问

1. **为什么不能纯粹用贪心？** 贪心只在 canonical 面额集合上最优；Part 2 故意给出反例
   `{1,3,4}`。判断一个集合是否 canonical 本身是一个不平凡的问题（Pearson 1994 有一个
   `O(d^3)` 的判定算法），面试里不需要展开，只需要知道"不确定就用 DP"。
2. **`window` 上界能不能证明？** 对一般面额集合证不出干净的上界（`dp` 非单调），只能经验验证 +
   用更大窗口的测试兜底；如果追问"能不能形式化"，诚实回答"需要面额集合的额外结构（比如包含 1
   且是 canonical）才有紧的证明，本题没有假设这些"。
3. **付款次数有限（比如钱包里每种面额只有有限张）怎么办？** 变成有界背包版本的零钱兑换，DP 状态要
   加一维"剩余张数"，或者对每种面额做单调队列优化的多重背包。
4. **能不能只算总数不构造具体拆法（Part 1/2），但 Part 3 要构造——两者复杂度一样吗？** 一样，DP
   表本来就存了转移信息，回溯只是多一个 `O(硬币数)` 的解码步骤，不增加渐进复杂度。

## 来源与置信度

- **MED**：TrueInterview 同步的 Snowflake Algo 87 题清单第 23 项「Min Coins with Change」，经
  `kevin-2023-code/Tech-Interview-Questions`（聚合站，题面付费，仅预览开头一句可见），见
  `../../../catalog/raw/github_repos.md` §2 第 23 行、§3 "pc23"。
- 预览只给出"面额固定 `{1,5,10,50,100,200}`，可多付找零，最小化硬币总数"这一句；Part 1 的搜索
  上界证明、Part 2 的任意面额集合、Part 3 的具体拆法构造均为重建，已标注 **(reconstructed)**。

## 考什么

S08（零钱兑换的双向 DP 变体，付款和找零都要 DP，不能想当然套贪心）· 上界论证的诚实表达（证不出来
就说证不出来，用经验验证 + 测试兜底）· DP 回溯构造具体解（不仅要最优值，还要一组见证）。
