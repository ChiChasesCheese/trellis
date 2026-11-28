---
id: mlp-coding-pc05-followups
node: coding.pc05
step: 2
type: qa
---
## Q
**子数组和：追问与变体**｜编程轮

写完"和能被 K 整除"后，面试官会接着问哪些变体和追问？

## A
- **和恰好为 K 的子数组个数（LC 560）：** 不取余，记每个前缀和出现的次数；当前前缀和为 `P`，就加上 `P - k` 出现过的次数。k 可正可负可为 0。

```python
def count_sum_k(nums, k):
    seen, prefix, count = {0: 1}, 0, 0
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)     # 找之前和为 P-k 的前缀
        seen[prefix] = seen.get(prefix, 0) + 1
    return count
```

- **和恰好为 K 的最长子数组：** 字典只记每个前缀和第一次出现的下标（后出现的只会让子数组更短），长度是 `r - l`；只在严格更长时更新答案，平局时保留最靠左的。

```python
def longest_sum_k(nums, k):
    first = {0: -1}          # 前缀和 -> 第一次出现的下标
    prefix, best = 0, (0, -1, -1)
    for r, x in enumerate(nums):
        prefix += x
        l = first.get(prefix - k)
        if l is not None and r - l > best[0]:
            best = (r - l, l + 1, r)         # (长度, 起点, 终点)
        first.setdefault(prefix, r)          # 只记第一次
    return best
```

- **为什么不用滑动窗口：** 数组有负数，窗口"右移变大、左移变小"的单调性不成立，必须用前缀和加哈希表。
- **负数取模：** Python 里对正 k 取模总是非负；C 和 Java 里 `%` 可能得负数，要写成 `((x % k) + k) % k`。
- **流式输入：** 三个版本都是单遍扫描，字典边来边更新，不需要回看历史数组。
- **记第一次还是最后一次：** 最长子数组要记第一次出现的下标；"最长无重复子串"记的是最后一次，方向相反，容易混。
- **会多花一个测试用例的边界：** 空数组返回 0；单个元素恰好满足；全零数组（每个子数组都满足）；`k=1`（所有子数组都满足）；没有满足的子数组时最长版本返回 `(0, -1, -1)`。

**英文答法。**
- "The array has **negatives**, so a sliding window doesn't work; prefix sums with a hashmap do."
- "For the longest subarray I keep only the **first** index of each prefix sum, since a later one can only shorten it."
- "It's a **single pass**, so it also works on a stream."
