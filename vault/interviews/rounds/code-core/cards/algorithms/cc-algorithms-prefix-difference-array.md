---
id: cc-algorithms-prefix-difference-array
node: algorithms.prefix
type: qa
---
## Q
m updates of the form "add v to every index in `[l, r]`" over an array of n, then read every cell. Both m and n are 10^5.

## A
**A difference array: record only the boundaries, integrate once.**

```python
diff = [0] * (n + 1)
for l, r, v in updates:
    diff[l] += v
    diff[r + 1] -= v            # the r+1 slot is why the array has n+1 entries
a = list(accumulate(diff[:n]))
```

- O(n + m) instead of O(n·m).
- Sizing the array `n` instead of `n + 1` is the standard crash, on exactly the update that touches the last index.
- It works only when **all** updates are applied before any read; interleaved reads and updates need a Fenwick tree instead.
- On large or sparse coordinates, keep a dict of `coordinate -> delta`, sort the keys, and sweep — that is the same idea and it is exactly the boundary sweep used for interval unions ([[cc-chrono-intervals-subtract-sweep]]).

## Q zh
在长度为 n 的数组上做 m 次「给 `[l, r]` 内每个下标加 v」的更新，然后读取每个格子。m 和 n 都是 10^5。

## A zh
**差分数组：只记录边界，最后积分一次。**

```python
diff = [0] * (n + 1)
for l, r, v in updates:
    diff[l] += v
    diff[r + 1] -= v            # 正是这个 r+1 的槽位让数组有 n+1 个元素
a = list(accumulate(diff[:n]))
```

- O(n + m)，而不是 O(n·m)。
- 把数组开成 `n` 而不是 `n + 1` 是标准的崩溃点，且恰好在触及最后一个下标的那次更新上。
- 它只在**所有**更新都先于任何读取时成立；读写交错则要改用树状数组。
- 坐标很大或稀疏时，维护 `坐标 -> 增量` 的 dict，对 key 排序后扫描 —— 这是同一个思路，也正是区间并集所用的边界扫描（[[cc-chrono-intervals-subtract-sweep]]）。
