# q04 · Maximum Order Volume：加权区间调度，练的是"排序端点 + 二分找前驱"这套固定动作

> [!tldr]
> - 这题考的是：从一堆有时间窗口的电话里挑出互不重叠的子集，让订单量总和最大——经典加权区间调度
> - 三步套路：按结束时间排序 → 对每个区间二分找"最晚的不冲突前驱" → `dp[i] = max(不选, 选+dp[前驱])`
> - 最值得带走的一个模式：**零时长区间是空集，不参与任何冲突判断**——这是本题唯一真正的"坑"，不是算法难，是边界语义容易想当然

## 1. 题目在说什么（人话版）
每通电话占据一个左闭右开区间 `[start, start+duration)`，同一时刻只能处理一通电话。要从所有来电中
挑出互不重叠的一个子集，让选中电话的 `volume`（订单量）总和最大。端点相接（一通在 18 结束，下一通
在 18 开始）不算重叠。

三行小例子：
```
start=[10,5,15,18,30], duration=[30,12,20,35,35], volume=[50,51,20,25,10]
选下标1(5~17,51) + 下标3(18~53,25)：17<=18 不冲突，总和 76
答案：76
```

## 2. 读题：把文字变成模型
- **实体**：电话（`start`、`duration`、`volume`）。
- **输入长什么样**：`PART <1|2>` + `n` + `n` 行 `start duration volume`。
- **输出要什么**：一个整数，最大总订单量。
- **状态**：按结束时间排序后，`dp[i]` = 只考虑前 `i` 通电话（排序后）时能拿到的最大总量。
- **一句话建模**：这是标准的 **加权区间调度**——排序 + 二分找前驱 + DP，唯一特殊之处是 `duration=0`
  的电话占据空区间，永远不与任何电话冲突，必须无条件计入答案。

> [!note] 为什么选这个数据结构
> 按结束时间排序后，"不冲突的前驱"具有单调性：对每个电话 `i`，所有满足 `end<=start[i]` 的电话构成
> 排序数组的一个前缀，可以用 `bisect_right` 直接二分定位，不需要为每个电话线性扫描。`dp` 数组只需要
> "前 i 个（排序后）里的最优解"，一维就够，不需要记录具体选了哪些。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析 `n` 行 `(start,duration,volume)`，调 `part1`/`part2`，打印一个整数。
2. **Part 1 最小可用**：先处理零时长电话（无条件求和，剩下的电话继续走 DP），按结束时间排序，对每个
   电话线性往前扫最近的不冲突前驱，`dp[i]=max(dp[i-1], volume[i]+dp[pred])`。用官方样例验证。
3. **Part 2 叠加**：把"线性扫前驱"换成 `bisect_right(ends, starts[i], 0, i)`，其余 DP 结构不变。
4. **收尾**：确认全重叠（答案=单个最大 volume）、全不重叠（答案=总和）、并列开始时间、大数值等边界。

## 4. 代码怎么组织
```
_split_free_and_normal(start,duration,volume) -> (free_sum, s',d',v')  # 剥离零时长电话
_sorted_by_end(start,duration,volume) -> (ends, starts, vols)          # 按结束时间排序
part1(...) -> int     # 线性扫前驱的 DP，正确优先
part2(...) -> int     # bisect_right 找前驱的 DP，O(n log n)
main(stdin, stdout)   # 解析、分发
```
`_split_free_and_normal` 和 `_sorted_by_end` 是 part1/part2 共用的两个 helper——两版算法唯一的区别
就是"怎么找前驱"，把这一步隔离开，能让面试官一眼看出你是从 O(n) 前驱扫描升级到二分，而不是重写了整个算法。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def _split_free_and_normal(start, duration, volume):
    free = 0
    ns, nd, nv = [], [], []
    for s, d, v in zip(start, duration, volume):
        if d == 0:                          # 空区间，永不冲突，无条件计入
            free += v
        else:
            ns.append(s); nd.append(d); nv.append(v)
    return free, ns, nd, nv

def _sorted_by_end(start, duration, volume):
    order = sorted(range(len(start)), key=lambda i: (start[i] + duration[i], start[i]))
    ends = [start[i] + duration[i] for i in order]
    starts = [start[i] for i in order]
    vols = [volume[i] for i in order]
    return ends, starts, vols

def part2(start, duration, volume):
    free, start, duration, volume = _split_free_and_normal(start, duration, volume)
    n = len(start)
    if n == 0:
        return free
    ends, starts, vols = _sorted_by_end(start, duration, volume)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        pred = bisect_right(ends, starts[i - 1], 0, i - 1)   # 最晚的不冲突前驱数量
        dp[i] = max(dp[i - 1], vols[i - 1] + dp[pred])
    return free + dp[n]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认：区间是左闭右开，端点相接不算冲突；`duration=0` 的电话占据空区间，我打算把它们
  单独摘出来无条件计入答案，剩下的走标准加权区间调度。」
- 写 Part 1 时：「按结束时间排序后，`dp[i]` 表示只看前 i 个（排序后）电话的最优解，对每个电话我先
  用线性扫描找最近的不冲突前驱，保证正确性。」
- 写 Part 2 时：「结束时间排好序之后，『不冲突的前驱』就是数组里的一个前缀，可以直接 `bisect_right`
  二分，把找前驱的复杂度从 O(n) 降到 O(log n)，总体 O(n log n)。」
- 交付时：「官方样例、全重叠、全不重叠都过了；Part 2 在 1e5 条记录上跑了性能测试，远低于预算。」

## 7. 常见跑偏（方法层面，3 条）
- **把零时长电话直接套进"end<=start"的通用判定式**：`duration=0` 的电话既不满足"结束<=某电话开始"
  也不满足"某电话结束<=它的开始"，通用公式会误判为冲突。必须先单独摘出来无条件计入。
- **排序 key 只用结束时间，不管开始时间的 tie-break**：结束时间并列时如果 key 不稳定，二分结果可能
  不一致（虽然本题最终答案不受影响，但排序 key 写全更稳妥）。
- **在 Part 1 就直接写二分**：面试官想看到你先给出"正确、朴素"的版本，再升级到二分，一步到位容易在
  中途卡壳时拿不到部分分。

## 8. 同族题 / 延伸
- 这是"加权区间调度"的标准模型（S03），同族题包括会议室安排、任务调度类问题——核心动作永远是
  "排序端点 + 二分找前驱 + DP"。
- 延伸思考：如果要求返回被选中的电话下标而不仅是总量，需要在 `dp` 之外额外记一个 `choice[i]` 数组，
  回溯重建路径。
- 练习命令：`python3 loop/mock.py start q04`
