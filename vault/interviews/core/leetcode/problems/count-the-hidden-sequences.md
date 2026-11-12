---
slug: count-the-hidden-sequences
---
## Q
**LC 2145 统计隐藏数组数目**｜Medium

隐藏数组 `hidden` 满足 `differences[i] = hidden[i+1] - hidden[i]`，且所有元素都在 `[lower, upper]` 内。求这样的数组有几个。

## A
**一句话。** 数组形状由前缀和固定，答案是起点能平移的位置数 `(upper - lower) - (max - min) + 1`。

```python
def number_of_arrays(differences, lower, upper):
    prefix = [0, *accumulate(differences)]   # 别漏开头的 0
    spread = max(prefix) - min(prefix)
    return max(0, (upper - lower) - spread + 1)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 前缀和漏掉开头的 `0`：`[1,2]`、`lower=1`、`upper=3` 应为 `0`，漏掉后跨度只算 `2`，返回 `1`。
- 不与 `0` 取最大：`([4,-7,2], 3, 6)` 公式值是 `-3`，应返回 `0`。

**追问。**
- 不想存 `prefix`？：边累加边维护当前值、最大值、最小值，`O(1)` 额外空间。
- 要列出所有隐藏数组？：起点取 `lower - min(prefix)` 到 `upper - max(prefix)`，各加上 `prefix`。

**同模式。** LC 303 区域和检索、LC 53 最大子数组和、LC 1094 拼车、LC 370 区间加法
