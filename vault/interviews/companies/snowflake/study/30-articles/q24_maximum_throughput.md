# q24 · Maximum Throughput：练的是"二分答案 + 反证法证明方案紧致"

> [!tldr]
> - TrueInterview 同步清单 #74（题名转述，无报告日期，本 kit 缺口补建）；**升级公式、二分实现与 Part 2 方案重建均为 (reconstructed)**
> - 这题考的是：预算内升级流水线各服务，最大化瓶颈（最小值）吞吐量——"最大化最小值"系列的标准形状
> - 三步套路：识别"最大化瓶颈"→二分答案 → 写出单调的 `feasible(T)` → 用反证法说明方案的瓶颈恰好等于二分找到的值
> - 最值得带走的一个模式：**"最大化最小值/最小化最大值"系列问题，只要能写出关于候选答案单调的可行性判断，就应该二分答案而不是直接构造**

## 1. 题目在说什么（人话版）

一条流水线由 `n` 个串联服务组成，整条流水线的吞吐量是所有服务里最小的那个（瓶颈）。
每升级服务 `i` 一次要花 `scalingCost[i]`，升级 `x` 次后它的产能变成 `throughput[i]×(1+x)`。
给定预算 `B`，怎么分配升级次数使瓶颈最大？

```
throughput=[2,10], scalingCost=[1,100], budget=5
把预算全给服务0：升级4次到 2×5=10，服务1不动 -> 瓶颈 10
```

## 2. 读题：把文字变成模型

- **实体**：`n` 个服务，每个有 `(throughput, scalingCost)`；共享预算 `B`；目标是最大化 `min(所有服务产能)`。
- **状态**：对候选目标值 `T`，每个服务达到 `≥T` 所需的最小升级次数和花费——这一步是独立的，不需要记忆之前的选择。
- **一句话建模**：这是一个 **二分答案 + 独立可行性判断** 的"最大化最小值"问题。

> [!note] 为什么用二分而不是直接贪心分配预算
> 因为升级公式是乘法关系（`throughput × (1+x)`），每次升级的边际提升是递减的，不存在
> 简单的"性价比排序"贪心。但可行性判断 `feasible(T)`——"每个服务独立算出达到 `T` 的
> 最小花费，加起来是否 `≤ B`"——对 `T` 是单调的（`T` 越大越难满足），单调性一旦成立，
> 二分答案就是标准解法。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **先写 `feasible(T)`**：`x_i = max(0, ceil(T/throughput[i]) - 1)`，花费 `x_i × scalingCost[i]`，求和跟预算比较。
2. **Part 1 最小可用**：对 `T` 二分（下界是原始最小值，上界用"预算全给某个服务"估计一个安全值），找最大可行 `T`。
3. **Part 2 叠加**：用最优 `T*` 对每个服务独立算出 `x_i`，就是达成 `T*` 的一组方案，不需要重新搜索。
4. **收尾**：口头论证"这组方案的实际瓶颈恰好等于 `T*`"——反证法：假设所有服务都严格超过 `T*`，那这组方案（花费不变）也证明了某个更高目标可行，矛盾。

## 4. 代码怎么组织

```
_validate(throughput, scaling_cost, budget)
_upgrades_needed(t, target) -> int              # 达到 target 至少要升级几次
_cost_for_target(throughput, scaling_cost, target, budget) -> (bool, int)  # feasible(T)
max_min_throughput(throughput, scaling_cost, budget)             # Part 1：二分
max_min_throughput_with_plan(throughput, scaling_cost, budget)   # Part 2：复用 Part 1 + 逐服务算方案
part1 / part2
```
`_upgrades_needed` 和 `_cost_for_target` 是二分内层调用的纯函数，Part 2 直接复用
`_upgrades_needed` 对最优 `T*` 重新算一遍每个服务的升级次数，不需要额外搜索。

## 5. 核心代码骨架

```python
def _upgrades_needed(t, target):
    # 达到 target 的最小非负升级次数：t * (1 + x) >= target
    if t >= target:
        return 0
    return -(-target // t) - 1   # ceil(target / t) - 1

def _cost_for_target(throughput, scaling_cost, target, budget):
    total = 0
    for t, c in zip(throughput, scaling_cost):
        total += _upgrades_needed(t, target) * c
        if total > budget:
            return False, total
    return True, total

def max_min_throughput(throughput, scaling_cost, budget):
    # Part 1：对候选瓶颈 T 二分，feasible(T) 越大越难满足
    lo = min(throughput)
    hi = max(t * (2 + budget) for t in throughput)   # 安全上界
    while lo < hi:
        mid = (lo + hi + 1) // 2
        feasible, _ = _cost_for_target(throughput, scaling_cost, mid, budget)
        if feasible:
            lo = mid
        else:
            hi = mid - 1
    return lo

def max_min_throughput_with_plan(throughput, scaling_cost, budget):
    # Part 2：对最优 T* 逐服务独立算出升级次数，就是一组达成方案
    target = max_min_throughput(throughput, scaling_cost, budget)
    upgrades = [_upgrades_needed(t, target) for t in throughput]
    return target, upgrades
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「这是最大化最小值的形状，我打算二分答案，先写 `feasible(T)`。」
- 写 Part 1 时：「`feasible` 对 `T` 单调不增，所以二分找最大可行 `T` 是 `O(n log(值域))`。」
- 引出 Part 2 时：「用最优 `T*` 独立算每个服务的升级次数就是一组方案；我可以用反证法说明这组方案的实际瓶颈恰好等于 `T*`，不会更高也不会更低。」

## 7. 常见跑偏（方法层面，3 条）

- 二分上界估计过小（比如直接用 `max(throughput)`），漏掉预算很大时可以远超原始最大值的情况。
- Part 2 里重新对每个服务做一次独立的二分/搜索，而不是直接复用 `feasible(T)` 里已经算过的 `_upgrades_needed` 公式。
- 说不清楚"为什么方案的瓶颈恰好等于 `T*`"，只会喊"因为二分找到的就是最优"，没有给出反证法。

## 8. 同族题 / 延伸

- "最大化最小值/最小化最大值"系列的标准套路，同族题：LC 1552 Magnetic Force；一维两遍扫描/多源 BFS 系列（`q25`）虽然是不同问题，但同样属于"先想清楚单调性再选算法"的方法论。
- 练习命令：`python3 drill.py start q24`
