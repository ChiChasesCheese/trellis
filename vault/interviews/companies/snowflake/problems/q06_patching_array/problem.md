# q06 · Patching Array — LC 484 原题 + 追问返回值列表

**Type:** LC 原题（精确复用）· **Stage:** 电面（历史）/ OA 题库 · **Skill:** S08（LC 原题 + 追问）

## 背景
本题就是 LeetCode 484 "Patching Array"，Snowflake 在 2019 年电面中原样问过（同一场电面还
考了另一题的 inorder→Morris traversal），2023 年 Canada OA 索引里也出现过（直接引用
LeetCode 链接）。`part2` 是一个自然的追问变体（本题作者重建）：不要求只返回补丁数量，而是
要求返回具体补丁了哪些值。

> LC 484 原题描述："Given a sorted integer array `nums` and an integer `n`, add/patch
> elements to the array such that any number in the range `[1, n]` inclusive can be formed
> by the sum of some elements in the array. Return the minimum number of patches required."

## 输入格式（stdin，用于 `main`）
```
PART <1|2>
n
nums（空格分隔，可以是空行表示空数组）
```
`nums` 已经是**升序排序**好的（LC 原题前提）。输出：
- `PART 1`：一个整数（补丁数量），末尾换行。
- `PART 2`：补丁值列表，空格分隔（空列表输出一个空行），末尾换行。

## 规则

### Part 1 — 标准贪心（LC 484 原题）
`part1(nums: list[int], n: int) -> int`：维护 `miss`（当前能确定"可以被凑出"的最小正整数
的下一个缺口，初值 `1`）、`i=0`、`patches=0`。当 `miss <= n` 时循环：
- 若 `i < len(nums)` 且 `nums[i] <= miss`：说明这个真实元素能扩展可覆盖区间，
  `miss += nums[i]; i += 1`。
- 否则：必须打一个补丁——概念上补丁值就是当前的 `miss`，打上之后可覆盖区间翻倍，
  `miss *= 2; patches += 1`。

循环结束（`miss > n`）后返回 `patches`。

### Part 2 — 返回补丁值列表（本题重建的追问）
`part2(nums: list[int], n: int) -> list[int]`：完全相同的贪心，唯一区别是每次需要打补丁
时，把**打补丁前的 `miss` 值**追加进结果列表，再翻倍。必须与 `part1` 保持一致：
`len(part2(nums, n)) == part1(nums, n)` 对任意输入恒成立。

## Worked Examples

**验证过的官方样例**（贪心手算，必须精确匹配）：
```
nums=[1,3], n=6      -> part1 = 1, part2 = [2]
nums=[1,5,10], n=20  -> part1 = 2, part2 = [2,4]
nums=[1,2,2], n=5    -> part1 = 0, part2 = []
```

**追加样例 1**：`nums=[], n=7`（手算贪心过程）：
```
miss=1 -> 无元素可用 -> 补1，miss=2，patches=1
miss=2 -> 补2，miss=4，patches=2
miss=4 -> 补4，miss=8，patches=3
miss=8 > 7 -> 停止
```
`part1([], 7) = 3`，`part2([], 7) = [1, 2, 4]`。

**追加样例 2**：`n=0`（边界）：循环条件 `miss <= n` 即 `1 <= 0`，一开始就为假，循环一次都
不执行 → 不论 `nums` 是什么，`part1(nums, 0) = 0`，`part2(nums, 0) = []`。

## 隐藏测试边界清单
- `n=0`：无论 `nums` 是什么，答案恒为 `0` / `[]`
- `nums` 为空数组
- `nums` 已经完全覆盖 `[1,n]`（0 个补丁），例如 `[1,2,4,8]` 覆盖 `[1,15]`
- 很大的 `n`（最高到 `2**31`），要求 `O(log n)` 贪心而不是暴力枚举——补丁数量约为
  `log2(n)`，即使 `nums` 为空也必须在极短时间内跑完
- `nums` 中含有 `1`（贪心要能从 1 开始覆盖，否则第一步必打补丁）
- `nums` 中含有比 `n` 还大的值（这些值永远不会被消费，因为 `miss` 从不会追上它们，
  贪心必须正确"跳过"它们而不是提前终止或出错）
- `part2` 长度必须等于 `part1` 的返回值，对任意输入恒成立

## 变体
- 原始电面帖子（2019）里，同一位面试官紧接着问了"数组差分去重 → 中序遍历 → Patching
  Array"三连，属于同一场电面的题目链（见 `catalog/CATALOG.md` pc08）。
- LeetCode 官方还有"返回打了哪些补丁"的类似追问（本题 part2 的原型）。

## 来源与置信度
- https://leetcode.com/problems/patching-array/ （HIGH，原题精确复用）
- https://leetcode.com/discuss/interview-question/424385/snowflake-phone-screen-patching-array/
  （2019 电面面经，HIGH，同帖还提到 inorder/Morris 题——即 q07 的来源，是同一场电面的
  姊妹题）
- 2023 Canada OA 题库索引 #7（HIGH，直接引用 LeetCode 原题链接）

**置信度：高** — 这是 LeetCode 原题精确复用，题面、样例、复杂度要求都可以直接对照官方
LeetCode 题库核实；`part2`（返回补丁值列表）是本题作者基于常见追问模式重建的合理变体，
未在原始面经中逐字出现。

## 考什么
- S08：LC 原题 + 复杂度再压一档（这里是贪心 `O(len(nums) + log n)`，而不是暴力枚举/回溯）
- 贪心不变量的维护与证明（`miss` 表示"当前保证可达的区间上界+1"）
- 边界处理：`n=0`、空数组、已完全覆盖、无关的大数值元素
- 两个 part 之间共享同一套贪心逻辑，只是收集的信息不同（计数 vs 具体值）
