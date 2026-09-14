# pc06 · Happy Number — O(n) → O(1) 空间 → 推广到任意进制与幂次

> 20 分钟题（常作为电面 / onsite 第一轮的"热身 + follow-up"）。Part 1、Part 2 是一手报道的原题与原追问；Part 3 **(reconstructed)**。

## 背景

2026 夏一位 Snowflake 候选人（"General Store Interview"）第一轮：**先聊约 20 分钟项目**，然后 coding 题 **Happy Number，先给出 O(n) 解，再被要求优化到 O(1)**；第二轮是系统设计"用户密码存储"（本 kit `sd09`）。

这题的考点不是数学，是**认出"迭代一个函数"就是一条隐式链表，判环可以不用额外空间**。

## 定义

`f(n)` = `n` 的各位数字平方和。从正整数 `n` 出发反复做 `n ← f(n)`：
- 能到 `1` → **happy**；
- 否则会陷入一个不含 1 的循环（十进制下就是 `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4`）。

为什么一定会进环：一个 d 位数的 `f` 值至多 `81·d`，大数迅速变小，之后只在有限范围内打转。

## API 契约（英文签名）

```python
def is_happy_set(n: int) -> bool
def is_happy_floyd(n: int) -> bool
def cycle_info(n: int, base: int = 10, power: int = 2) -> tuple[int, int]
```
`n < 1` → `ValueError`。

## 规则

### Part 1 — 任意正确解法

用一个集合记录见过的数，出现重复即进环。时间与空间都与"尾巴 + 环长"成正比。

### Part 2 — O(1) 额外空间（一手原追问）

**不许用 set / dict / 会增长的 list。** 提示：把 `n → f(n) → f(f(n)) → …` 看成链表，快慢指针（Floyd）：慢的每次走一步、快的每次走两步，必在环内相遇；相遇点是 1 就是 happy。

### Part 3 — 任意进制、任意幂次，报告环 **(reconstructed)**

`f(n)` = `n` 在 `base` 进制下各位数字的 `power` 次方和。返回 `(环长, 环中最小值)`。仍要求 O(1) 额外空间。`base < 2` 或 `power < 1` → `ValueError`。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**：`19 → 82 → 68 → 100 → 1` → `is_happy_* (19) = True`，`cycle_info(19) = (1, 1)`
**例 2**：`2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 …` → `False`，`cycle_info(2) = (8, 4)`
**例 3**：1–50 中的 happy 数：`[1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49]`
**例 4**：`cycle_info(153, 10, 3) = (1, 153)`（`1³+5³+3³ = 153`，自反点，即 Armstrong 数）
**例 5**：`cycle_info(5, 2, 2) = (1, 1)`（二进制下数字只有 0/1，平方和就是 1 的个数，最终都到 1）

## `main()` 命令流

```
PART 1        PART 2        PART 3
19            7             2 10 2
2             116           153 10 3
→ true        → true        → 8 4
  false         false         1 153
```

## 边界清单

- `n = 1`（本身就是 1）
- 极大 `n`（`10^300`、`2·10^300`）——Python 大整数没问题，关键是第一步就变小
- `n ≤ 0` → `ValueError`
- Part 2 被检查"没有建集合 / 字典"（测试会把模块里的 `set`、`dict` 替换成报错函数）
- Part 3 自反点（环长 1）与二进制退化情形
- Part 3 非法 `base` / `power`

## 追问

1. **为什么 Floyd 一定会相遇？** 进环后快指针每步相对慢指针靠近 1 步，环长有限。
2. **相遇点一定是环的入口吗？** 不一定；要找入口，把一个指针放回起点、两者同速走，再次相遇即入口（本题不需要）。
3. **有没有更快的判定？** 十进制平方和版本里，不 happy 的序列必经过 4，所以"走到 1 或 4 就停"是 O(1) 空间的特判——但它依赖这个具体函数，面试里先讲 Floyd 再提特判。
4. **Brent 算法和 Floyd 的区别？** Brent 以 2 的幂次移动"传送点"，函数调用次数更少；本题规模下差别不大。

## 来源与置信度

- **HIGH（一手）**：1point3acres thread-1179571（2026 夏），经 Telegram 镜像 t.me/s/usinterview/28738："Coding: Happy Number problem (optimized to O(1)); System Design: User password storage system"，前约 20 分钟讨论项目。见 `../../../../raw/process_research.md` §3.2 #2 与 `../../../../catalog/raw/system_design.md` §1.9。
- LC 202 官方题面：https://leetcode.com/problems/happy-number/
- Part 3 为重建。

## 考什么

S08 LC 原题 + 复杂度再压一档（O(n) 空间 → O(1)）· S05 判环（与链表判环同一招）· 在 20 分钟内说清为什么一定会进环。
