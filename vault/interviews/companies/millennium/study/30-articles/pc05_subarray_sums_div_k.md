# pc05 · Subarray Sums Divisible by K：练的是"子数组和 = 两个前缀和的差"

> [!tldr]
> - 这题考的是：把"子数组的和"翻译成"两个前缀和的差"，剩下就是数一数哈希表
> - 三步套路：先想清楚 `P[r] - P[l]` 表达的是什么子数组 → 跑通计数版 → 把"计数"换成"记第一次出现的下标"就拿到最长版
> - 最值得带走的一个模式：**任何"子数组和满足某条件"的题，先写出前缀和数组，再看条件变成了前缀和之间的什么关系**

## 1. 题目在说什么（人话版）

给一个整数数组，问"和能被 K 整除的连续子数组有多少个"（Part 1）、"和恰好等于 K 的连续子数组有多少个"（Part 2）、"和恰好等于 K 的连续子数组里最长的是哪个"（Part 3）。

```
nums = [4, 5, 0, -2, -3, 1], k = 5
子数组 [5], [0], [-2,-3], [4,5,0,-2,-3,1], … 一共 7 个和能被 5 整除
```

暴力做法是枚举所有 `(i, j)` 子数组、逐个算和，O(n²)。三个 part 都能压到 O(n)。

## 2. 读题：把文字变成模型

- **实体**：数组 `nums`；前缀和数组 `P`，`P[0] = 0`，`P[i] = nums[0] + … + nums[i-1]`。
- **关键翻译**：子数组 `nums[l..r-1]`（对应下标 `(l, r]`）的和就是 `P[r] - P[l]`。一旦这样写，"子数组和"问题全部变成"两个前缀和数组元素的差"问题。
- **状态**：扫描到 `r` 时，只需要知道"前面出现过的 `P[l]` 都是什么"——这决定了用 dict。
- **一句话建模**：Part 1/2 是"数配对"，Part 3 是"找配对里跨度最大的那对，且要最左"。

> [!note] 为什么选哈希表
> 需要 O(1) 判断"某个前缀和值之前出现过没有、出现了几次、第一次在哪"。数组或排序都做不到边扫边查 O(1)，dict 可以。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`main()` 读入 → 每两行解析成 `(nums, k)` → 调 `part1` → 打印。
2. **Part 1 最小可用**：`seen = {0: 1}`；扫描时 `prefix = (prefix + x) % k`，先加 `seen.get(prefix, 0)` 再把当前余数计数 +1。立刻用题面样例自测（`[4,5,0,-2,-3,1], k=5` 应为 7）。
3. **Part 2 叠加**：去掉取模，`seen` 记"原始前缀和出现次数"；查 `prefix - k`。
4. **Part 3 叠加**：把"计数"换成"第一次出现的下标"（`{0: -1}` 起手），查到 `prefix - k` 就算长度，**严格更长才更新**——这一步顺带保证了并列时留住最左边那个,不用额外写 tie-break 逻辑。
5. **收尾**：k 的合法性校验写全（Part 1 的 k 是模数必须 ≥ 1；Part 2/3 的 k 是目标和可正可负可为 0）、空数组和单元素跑一遍。

## 4. 代码怎么组织

```
_check_nums(nums) / _check_k(k, positive_only)   # 输入校验集中一处
count_subarrays_div_k(nums, k)                    # Part 1：余数计数字典
count_subarrays_sum_k(nums, k)                    # Part 2：原始前缀和计数字典
longest_subarray_sum_k(nums, k)                   # Part 3：第一次出现下标字典 + 严格更长才更新
_parse_pairs(lines)                                # 两行一组：nums 行 + k 行
part1..part3 / main
```

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def count_subarrays_div_k(nums, k):
    seen = {0: 1}          # 前缀和余数 -> 出现次数
    prefix = 0
    count = 0
    for x in nums:
        prefix = (prefix + x) % k
        count += seen.get(prefix, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

def longest_subarray_sum_k(nums, k):
    first_seen = {0: -1}   # 前缀和 -> 第一次出现的下标
    prefix = 0
    best_len, best_start, best_end = 0, -1, -1
    for r, x in enumerate(nums):
        prefix += x
        l = first_seen.get(prefix - k)
        if l is not None and r - l > best_len:
            best_len, best_start, best_end = r - l, l + 1, r
        first_seen.setdefault(prefix, r)   # 只记第一次
    return best_len, best_start, best_end
```

## 6. Talking through it in the interview

- Before starting: "Let me translate this into prefix sums first — a subarray's sum is just the difference of two prefix sums, so I only need a hashmap of prefix sums I've seen."
- Writing Part 1: "I'm counting by residue mod k instead of the raw sum, because two subarrays cancel out to a multiple of k exactly when their prefix sums share the same residue."
- Writing Part 3: "For the longest version I only keep the *first* index each prefix sum was seen at — a later occurrence can only shorten the subarray, never lengthen it."
- On delivery: "The worked examples pass; if there's time I'd add a streaming variant that updates the same dict incrementally as new elements arrive."

## 7. 常见跑偏（方法层面，3 条）

- 一上来就想"滑动窗口"：这题的数组允许负数，滑动窗口的单调性假设不成立，前缀和 + 哈希表才是正解。
- Part 1 忘记 Python 的 `%` 对正 `k` 天然落在 `[0, k)`，反而手写了一套"修正负余数"的逻辑——多此一举，但要能讲出为什么在 C/Java 里就需要修正。
- Part 3 把"记第一次出现的下标"错记成"记最后一次出现的下标"（那是"最长无重复子串"用的技巧，方向正好相反，容易混）。

## 8. 同族题 / 延伸

- 本 kit `pc01_grouped_aggregation`：同样是"用 dict 边扫边计数/累加"的单遍扫描骨架，换成了分组求和而不是前缀和。
- 练习命令：`python3 loop/mock.py start pc05`
