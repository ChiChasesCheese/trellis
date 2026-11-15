---
slug: largest-positive-integer-that-exists-with-its-negative
---
## Q
**LC 2441 与对应负数同时存在的最大正整数**｜Easy

不含 `0` 的整数数组 `nums`。找出最大的正整数 `k`，使得 `-k` 也在数组中；没有返回 `-1`。

## A
**一句话。** 把数组放进集合，遍历正数，`-x` 在集合里就是候选，取最大。

```python
def find_max_k(nums):
    seen = set(nums)
    return max((x for x in nums if x > 0 and -x in seen),
               default=-1)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 不要求 `x > 0`：`x` 为负数时 `-x` 是正数，会返回负数。
- `max` 空序列报错：要给 `default=-1`。

**追问。**
- 想省空间？：排序后双指针，一个指最小的负数、一个指最大的正数，向中间夹。

**同模式。** LC 217 存在重复元素（Contains Duplicate）、LC 1 两数之和
