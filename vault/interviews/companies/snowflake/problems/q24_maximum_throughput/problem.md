# q24 · Maximum Throughput — 预算内升级流水线，最大化瓶颈吞吐

> OA 题（TrueInterview 同步清单 #74；本 kit 缺口补建）。Part 1 为原题（二分答案）；
> Part 2 **(reconstructed)**：返回达成最优解的具体升级方案。

## 背景

TrueInterview 清单 #74 "Maximum Throughput（流水线升级预算）"没有报告日期，只给出题名
和分类"Algo"。这个名字和"预算约束下最大化瓶颈"的形状，在 Snowflake 及同类公司的 OA
里高频出现（跟"maximize minimum"系列题——如 LC 1552 Magnetic Force——同族）。本 kit 按
标准的"二分答案 + 可行性校验"形状重建了完整题面、公式与全部样例。

一条流水线由 `n` 个串联的服务组成，整条流水线的吞吐量 = **所有服务里最小的那个**（瓶
颈）。服务 `i` 初始吞吐量 `throughput[i]`；每升级一次服务 `i` 花费固定的
`scalingCost[i]`，升级 `x` 次后它的产能变为 `throughput[i] × (1 + x)`
**（乘法关系为 (reconstructed)）**。给定总预算 `B`，在预算内选择怎么升级各服务，使瓶颈
吞吐量最大。

## 输入

- `1 ≤ n`，`throughput[i] ≥ 1`，`scalingCost[i] ≥ 1`，`budget ≥ 0`；
- 非法输入（长度不一致、`throughput < 1`、`scalingCost < 1`、`budget < 0`）抛
  `ValueError`。

## API 契约（英文签名）

```python
def max_min_throughput(throughput: list[int], scaling_cost: list[int], budget: int) -> int
def max_min_throughput_with_plan(throughput: list[int], scaling_cost: list[int], budget: int) -> tuple[int, list[int]]
```

## 规则

### Part 1 — 二分答案

对候选瓶颈值 `T`，服务 `i` 要达到 `≥ T` 至少需要升级
`x_i = max(0, ceil(T / throughput[i]) - 1)` 次，花费 `x_i × scalingCost[i]`；把所有服务
的花费加起来跟预算 `B` 比较，就是 `feasible(T)`。`T` 越大 `feasible` 越难满足（单调
不增），所以对 `T` 二分，找最大的可行 `T`。`O(n log(值域))`。

### Part 2 — 返回具体升级方案 **(reconstructed)**

二分找到最优 `T*` 后，对每个服务按上面的公式独立算出最小升级次数 `x_i`，就是一组
达成 `T*` 的方案；这组方案的**总花费一定 `≤ B`**（否则 `T*` 就不会被判定为可行）。

**为什么这组方案的实际瓶颈恰好等于 `T*`（不多不少）**：假设这组方案让所有服务的产能
都严格超过 `T*`，那这组方案同时也证明了某个 `> T*` 的目标是可行的（花费不变，因为
"最小升级次数"公式对更高目标只会要求更多升级，而这里已经达到了）——这与二分选出的
`T*` 是"最大可行值"矛盾。所以至少有一个服务的产能恰好落在 `T*`，也就是实际瓶颈
`= T*`。**这个论证本身就是本题的追问点**，出题人通常会问"你怎么知道这组方案不会不
小心把瓶颈做得比二分找到的答案更高/更低"。

Checker（也就是测试）拿到 `(T, upgrades)` 后会独立重算：`min(throughput[i] * (1 +
upgrades[i]))` 应该等于 `T`，且 `Σ upgrades[i] * scalingCost[i] ≤ budget`。

## Worked examples（全部由 `solution.py` 实际运行得出）

| throughput | scalingCost | budget | Part 1 | Part 2（方案） |
|---|---|---|---|---|
| `[2, 10]` | `[1, 100]` | 5 | `10` | `(10, [4, 0])` —— 服务 0 升级 4 次到 `2×5=10`，服务 1 不动；总花费 `4 ≤ 5` |
| `[2, 10]` | `[1, 100]` | 3 | `8` | 服务 0 升级 3 次到 `2×4=8`（升不到 9，因为 `x0=4` 时花费 4 超预算） |
| `[3, 7, 2]` | `[1, 1, 1]` | 0 | `2`（预算为 0，瓶颈就是原始最小值） | `(2, [0, 0, 0])` |
| `[1]` | `[1]` | 26 | `27`（`1×(1+26)`） | `(27, [26])` |

## `main()` 命令流

```
PART 1          PART 2
2 5             2 5
2 10            2 10
1 100           1 100
→ 10            → 10
                  4 0
```

## 边界清单

- `budget = 0`：答案就是原始 `min(throughput)`，方案全 0
- 升级昂贵服务不划算，只升级便宜服务追上瓶颈（`budget=3` 例，答案 `8` 不是 `10`）
- 只有一个服务（瓶颈就是它自己，方案是把全部预算花在它身上算出的最大升级次数）
- 所有服务吞吐量已经相等（升级任何一个都不会立即提升瓶颈，除非全部一起升）
- 方案自洽性：Part 2 返回的方案重算出的瓶颈必须**恰好等于** Part 1 的答案（不多不少）
- 非法输入：长度不一致、`throughput < 1`、`scalingCost < 1`、`budget < 0` → `ValueError`
- 性能：`n = 10⁵`，数值到 `10⁶`，`budget` 到 `10¹²` 时两个 Part 均 `< 2s`

## 追问

1. **为什么公式是 `throughput[i] × (1 + x)` 而不是 `throughput[i] + x`（线性）？** 如
   果是线性叠加，`feasible(T)` 的每次升级"性价比"（单位花费带来的产能增量）是常数，
   最优策略会退化成"贪心地把预算分配给性价比最高的服务"，不需要二分；乘法关系下增量
   递减（越往后升级带来的边际吞吐提升占比越小），二分答案 + 独立可行性判断才是标准
   解法，这也是这题被设计成乘法的原因。
2. **能不能不二分，直接用贪心/优先队列每次把预算给"最能提升瓶颈"的服务？** 可以，但
   要证明"每次都把一次升级次数给当前瓶颈服务"是正确贪心（类似"分糖果"类贪心），且
   要处理"当前瓶颈服务升级一次花费太高、不如升级另一个服务追上来"这类比较，实现复杂
   度不比二分低，二分更直接。
3. **如果升级有次数上限（每个服务最多升级 `k` 次）呢？** `feasible(T)` 里的
   `x_i = min(需要的次数, k)`，超过上限就直接判定该目标对该服务不可行（如果算出来的
   `x_i` 本身就超过 `k`）。
4. **多个服务并列瓶颈时，方案是否唯一？** 不唯一——只要总花费不超预算、且都达到
   `T*`，具体怎么分配"剩余预算"（没花完的部分）在多个可行方案间可以不同；本题只要求
   给出**一个**可行且达到最优瓶颈的方案，Checker 不检查方案的唯一性。

## 来源与置信度

- **MED（聚合站转述，公式与算法为重建）**：GitHub 镜像
  [`kevin-2023-code/Tech-Interview-Questions` `companies/snowflake.md`](https://github.com/kevin-2023-code/Tech-Interview-Questions/blob/main/companies/snowflake.md)
  第 74 行 "Maximum Throughput"；映射见 `../../catalog/raw/github_repos.md` §2、§3。
- 升级公式（乘法关系）、二分答案的具体实现与 Part 2 的方案重建，均标注 **(reconstructed)**。

## 考什么

二分答案 + 独立可行性判断（"最大化最小值"系列的标准形状）· 用反证法论证"方案的瓶颈
恰好等于二分找到的最优值"· 大数值下二分上界的安全估计。
