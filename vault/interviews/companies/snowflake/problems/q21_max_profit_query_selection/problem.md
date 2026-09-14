# q21 · Maximum Profit Query Selection — 只跑一种查询类型，怎么选最赚

> OA 题（TrueInterview 同步清单 #54，2026-01 报告，本 kit 缺口补建）。Part 1 为原题
> （选一种类型）；Part 2 **(reconstructed)**：预算可以拆给两种不同类型。

## 背景

TrueInterview 通过 GitHub 镜像（`kevin-2023-code/Tech-Interview-Questions`）同步的 87 题
清单里 #54"Maximum Profit Query Selection"，报告于 2026-01：有 `n` 种查询类型，第 `i`
种每跑一次要花 `durations[i]` 单位时间、赚 `revenues[i]`；给定总时间预算 `k`，**只能选一
种类型反复跑**，跑 `floor(k / durations[i])` 次，求能拿到的最大利润。预览未给出具体样
例，本 kit 按标准形状重建题面与全部样例。

## 输入

- `1 ≤ n`，`durations[i] ≥ 1`，`revenues[i] ≥ 0`，`k ≥ 0`；
- 非法输入（长度不一致、`duration < 1`、`revenue < 0`、`k < 0`）抛 `ValueError`。

## API 契约（英文签名）

```python
def max_profit_single(durations: list[int], revenues: list[int], k: int) -> int
def max_profit_two_types(durations: list[int], revenues: list[int], k: int) -> int
```

## 规则

### Part 1 — 只选一种类型（原题）

对每种类型 `i` 算出 `floor(k / durations[i]) * revenues[i]`，取最大值。`O(n)`。

### Part 2 — 预算可拆给至多两种不同类型 **(reconstructed)**

同一个预算 `k` 可以拆成两段分别给两种不同类型 `i, j`（`i ≠ j`）：用 `k1` 时间跑
`floor(k1/durations[i])` 次类型 `i`，剩下 `k - k1` 时间跑类型 `j`，最大化两者收益之和。
这是"恰好两种物品、数量不限"的**无界背包**问题——对每一对 `(i, j)` 单独做一次容量为
`k` 的无界背包 DP，取所有 pair 的最优值，再跟 Part 1 的单类型最优比较取大（因为"混着
跑"不一定比"只跑一种"好）。

**关键事实**：混着跑有可能严格更优。例：`durations=[3,4]`, `revenues=[4,5]`, `k=7`。只
跑一种：`floor(7/3)*4=8` 或 `floor(7/4)*5=5`，最优 `8`；各跑一次（`3+4=7`）：
`4+5=9 > 8`。**"只选收益率最高的那种"不是正确贪心**（跟 q19 的"只翻倍最大元素不是最
优贪心"是同一类教学点：局部最优单类型 ≠ 全局最优）。

复杂度：`O(n² · k)`（每对 `O(k)` 背包），题面把 Part 2 的规模刻意限制到
`n ≤ 30`、`k ≤ 2000`、`durations[i], revenues[i] ≤ 200`，使其在秒级完成，也方便用独立的
暴力（对每对枚举类型 `i` 的跑动次数、贪心取满剩余预算给类型 `j`）交叉验证。

## Worked examples（全部由 `solution.py` 实际运行得出）

| durations | revenues | k | Part 1 | Part 2 |
|---|---|---|---|---|
| `[3, 4]` | `[4, 5]` | 7 | `8`（跑 2 次时长 3 的类型） | `9`（两种各跑一次） |
| `[3, 5]` | `[10, 11]` | 10 | `30`（跑 3 次时长 3 的类型） | `30`（混着跑没有更优） |

## `main()` 命令流

```
PART 1              PART 2
2 7                 2 7
3 4                 3 4
4 5                 4 5
→ 8                 → 9
```

## 边界清单

- 混着跑严格更优（`[3,4],[4,5],7 → 8` vs `9`）
- 混着跑不比单类型更优（`[3,5],[10,11],10 → 30`，两个 Part 相等）
- `k = 0`
- 只有一种类型（Part 2 应退化为 Part 1 的答案）
- 某类型 `revenue = 0`（永远不会被选中，但不应干扰其余类型的计算）
- 非法输入：长度不一致、`duration < 1`、`revenue < 0`、`k < 0` → `ValueError`
- 性能：Part 1 `n = 10⁵`（大数值、Python 整数不溢出）`< 2s`；Part 2 在题面限定规模
  （`n ≤ 30`, `k ≤ 2000`）下 `< 2s`

## 追问

1. **为什么"只挑收益率最高的类型"不总是对？** 收益率 `revenues[i]/durations[i]` 最高
   的类型可能因为 `durations[i]` 太大而在预算 `k` 下"用不满"（余量被浪费），另一种类型
   哪怕收益率低一点，也可能把预算用得更满。
2. **能不能扩展到"最多选 m 种类型"？** 可以做成一般无界背包：对每种类型当成一个物
   品，`dp[c]` = 预算 `c` 内任意组合的最大利润，一次 `O(n·k)` DP 覆盖"选任意多种"，比
   Part 2 的"恰好两种"更宽松；如果题目要求"恰好/至多 m 种不同类型"，需要在状态里再加
   一维"已用的类型数"，变成 `O(n·k·m)`。
3. **如果 `durations[i]` 允许为 0（免费跑）呢？** 收益无穷大，需要在输入校验阶段单独
   处理（本题禁止 `duration < 1`，就是为了避开这个退化情况）。
4. **预算 `k` 大到 10⁹ 但只有个位数种类型呢？** Part 1 仍是 `O(n)`；Part 2 的背包 DP
   在容量维度上不可行（`O(k)` 太大），需要换成"对每对做数论意义上的整数规划"（枚举
   `k1 mod lcm(durations)` 范围内的余量），这是刻意留给更大规模追问的方向，不在本题的
   reconstructed 范围内。

## 来源与置信度

- **MED（聚合站转述，题面重建）**：GitHub 镜像
  [`kevin-2023-code/Tech-Interview-Questions` `companies/snowflake.md`](https://github.com/kevin-2023-code/Tech-Interview-Questions/blob/main/companies/snowflake.md)
  第 54 行 "Maximum Profit Query Selection"（2026-01 报告）；映射与可信度说明见
  `../../catalog/raw/github_repos.md` §2、§3。
- Part 2（拆预算给两种类型）为重建；原始预览只给出了"选一种类型"的题面。

## 考什么

无界背包 / 贪心陷阱（"只看收益率"不是正确贪心）· 复杂度刻意分级（大规模 Part 1 用
`O(n)`，小规模 Part 2 用 `O(n²k)`）· 用独立暴力（枚举 + 贪心取满剩余预算）交叉验证 DP。
