# q23 · Work Schedule：练的是"回溯剪枝天然给出字典序 vs 计数 DP 前缀和降复杂度"

> [!tldr]
> - TrueInterview 同步清单 #72（2025-07 报告，题名转述，本 kit 缺口补建）；**Part 2（长 pattern 计数取模 + 前缀和 DP）整体为 (reconstructed)**
> - 这题考的是：7 天排班表里 `?` 填 `0..dayHours`，凑出总工时 `workHours`，列出所有解（字典序）或只计数
> - 三步套路：升序回溯 + 区间可行性剪枝 → 意识到"升序 + 从左到右"天然给出字典序 → 大规模改成前缀和滑动窗口 DP
> - 最值得带走的一个模式：**"按数值/位置升序生成"本身就是排序，不需要事后再 `sorted()`——只要生成顺序和目标顺序对应，就不要多此一举**

## 1. 题目在说什么（人话版）

`pattern` 是恰好 7 个字符的排班表，每个字符要么是已定好的工时（`'0'`–`'8'`），要么是
待定的 `'?'`（可以填 `0` 到 `dayHours` 之间任意整数）。求所有让一周总工时恰好等于
`workHours` 的填法，按字典序排列。

```
pattern="??00000", workHours=3, dayHours=8
-> ["0300000", "1200000", "2100000", "3000000"]（字典序）
```

## 2. 读题：把文字变成模型

- **实体**：7 个位置，每个位置要么固定要么待定；一个目标总和 `workHours`。
- **状态**：递归到位置 `i` 时的"已用工时"，以及"剩余位置还能贡献的区间 `[lo, hi]`"。
- **一句话建模**：Part 1 是 **"按位置回溯 + 用区间上下界剪枝"**；Part 2 是 **"计数 DP，`?` 位置的转移是一次滑动窗口求和，用前缀和降复杂度"**。

> [!note] 为什么升序回溯天然给出字典序
> 排班字符串只在 `?` 位置变化，其余位置对所有解都相同。只要保证每个 `?` 位置的取值
> 按数值升序被尝试、且位置本身按从左到右递归，生成顺序天然和字符串的字典序比较完全
> 对应——不需要收集完所有解再 `sorted()`，这是"生成顺序 = 目标顺序"时最省事的写法。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：从左到右递归每个位置，`i == n` 时检查 `running == workHours` 就收集结果。
2. **Part 1 最小可用**：先写出不剪枝的暴力回溯（`?` 位置枚举 `0..dayHours`），用样例验证正确性和字典序。
3. **加剪枝**：用"后缀固定工时和"+"剩余 `?` 数 `× dayHours`"算出 `[lo, hi]`，`workHours` 不在区间内就剪枝，避免大量无效递归。
4. **Part 2 叠加**：换成 `dp[i][s]` 计数 DP；固定位是整体平移，`?` 位是宽度 `dayHours+1` 的滑动窗口和，用前缀和把每层降到 `O(S)`。

## 4. 代码怎么组织

```
_validate(pattern, work_hours, day_hours)
all_schedules(pattern, work_hours, day_hours)       # Part 1：回溯 + 剪枝，字典序天然生成
count_schedules_mod(pattern, work_hours, day_hours) # Part 2：dp[i][s] + 前缀和降复杂度
part1 / part2
```
Part 1、Part 2 是两条独立路径（一个要具体解、一个只要计数），没有共享 helper，但解决
的是同一个"约束求和"问题——面试里可以先提一句"如果只要计数，我会换成 DP"来预告 Part 2。

## 5. 核心代码骨架

```python
def all_schedules(pattern, work_hours, day_hours):
    # Part 1：回溯，'?' 按 0..day_hours 升序试 -> 输出天然字典序
    n, chars, out = len(pattern), list(pattern), []
    fixed = [0] * (n + 1); qs = [0] * (n + 1)   # 位置 i 之后：固定数字和、'?' 个数
    for i in range(n - 1, -1, -1):
        fixed[i] = fixed[i + 1] + (0 if pattern[i] == "?" else int(pattern[i]))
        qs[i] = qs[i + 1] + (pattern[i] == "?")

    def rec(i, run):
        if i == n:
            if run == work_hours: out.append("".join(chars))
            return
        for v in ([int(pattern[i])] if pattern[i] != "?" else range(day_hours + 1)):
            lo = run + v + fixed[i + 1]              # 后面 '?' 全填 0 的总和
            if lo > work_hours: break                # v 递增，lo 只会更大
            if lo + qs[i + 1] * day_hours < work_hours: continue   # 全填满也不够
            chars[i] = str(v); rec(i + 1, run + v)
        chars[i] = pattern[i]

    rec(0, 0)
    return out

def count_schedules_mod(pattern, work_hours, day_hours, MOD=1_000_000_007):
    # Part 2：dp[s] = 和为 s 的方案数；'?' 是宽 day_hours+1 的窗口和，前缀和 O(S)
    dp = [1] + [0] * work_hours
    for c in pattern:
        if c != "?":
            d = int(c); dp = [dp[s - d] if s >= d else 0 for s in range(work_hours + 1)]
            continue
        pre = [0]
        for x in dp: pre.append((pre[-1] + x) % MOD)
        dp = [(pre[s + 1] - pre[max(0, s - day_hours)]) % MOD for s in range(work_hours + 1)]
    return dp[work_hours]
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「我先写不带剪枝的回溯把样例跑通，再加区间剪枝。」
- 写 Part 1 时：「因为 `?` 是升序尝试、位置从左到右，生成的解已经是字典序，不需要再排序。」
- 引出 Part 2 时：「如果 pattern 变长到上千、只要计数不要具体方案，回溯的分支数会爆炸，我会换成 DP，`?` 位置的转移用前缀和把 `O(dayHours)` 降到 `O(1)` 均摊。」

## 7. 常见跑偏（方法层面，3 条）

- 先生成所有解再 `sorted()`，没意识到升序回溯已经天然给出字典序（浪费一次 O(n log n)）。
- 剪枝时算错区间（比如忘了加上后缀固定和），导致漏解或多算无效分支。
- Part 2 的 `?` 转移写成对每个 `s` 都重新累加窗口和（`O(dayHours)` 每格），没用前缀和优化，整体退化成 `O(n·S·dayHours)`。

## 8. 同族题 / 延伸

- 前缀和加速滑动窗口和的技巧同样适用于任何"转移是对前一状态某个定长区间求和"的 DP（求最值则要换单调队列）。
- 练习命令：`python3 drill.py start q23`

## 索引行

| [q23_work_schedule](q23_work_schedule.md) | `../../problems/q23_work_schedule/` | OA | "按数值/位置升序生成"本身就是排序，不需要事后再 `sorted()`——只要生成顺序和目标顺序对应，就不要多此一举 |
