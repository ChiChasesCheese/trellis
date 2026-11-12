---
slug: tt-most-frequent-ties-smaller
---
## Q
**出现次数最多的元素（并列取较小的）**｜Easy

整数数组 `nums`，返回出现次数最多的元素；并列时返回数值最小的。例：`[3,1,3,1,2]` → `1`。

## A
**一句话。** `Counter` 计数后用复合键 `(-次数, 数值)` 取 `min`，一次比较表达两条规则。

```python
def most_frequent(nums):
    count = Counter(nums)
    # 次数大的优先（取负），次数相同取数值小的
    return min(count, key=lambda x: (-count[x], x))
```

**复杂度。** 时间 `O(n)`，空间 `O(k)`。

**易错点。**
- 用 `most_common(1)`：并列时按首次出现顺序返回，`[3,1,3,1,2]` 得 `3`，应为 `1`。
- 键写成 `(count[x], x)` 取 `max`：并列时取到较大的值。

**追问。**
- 数据是流，随时回答？：维护计数和当前答案，新来 `x` 后若 `(count[x], -x)` 更大就更新，每次 `O(1)`。
- 要前 `k` 个？：`heapq.nsmallest(k, count, key=lambda x: (-count[x], x))`。

**同模式。** LC 347 前 K 个高频元素、LC 692 前 K 个高频单词、LC 895 最大频率栈、LC 169 多数元素
