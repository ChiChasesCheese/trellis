---
slug: kth-largest-element-in-an-array
---
## Q
**LC 215 数组中的第 K 个最大元素**｜Medium

返回数组排序后的第 `k` 个最大元素（重复值各算一个），要求平均 `O(n)`。

## A
**一句话。** 快速选择（quickselect）：随机 pivot 三路划分，只钻进答案所在的那一堆。

```python
def find_kth_largest(nums, k):
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):             # 答案在大堆
            nums = bigger
        elif k <= len(bigger) + equal:   # 就是 pivot
            return pivot
        else:                            # 答案在小堆
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```

**复杂度。** 时间 期望 `O(n)`，最坏 `O(n^2)`，空间 `O(n)`。

**易错点。**
- 不把相等值单独成一段：全相同的数组每轮只排除一个元素，退化成 `O(n^2)`。
- 进小堆时漏减 `k`：`[3,2,1]`、`k=3`、pivot 为 `2`，小堆里的 `k` 应是 `1`，答案 `1`。
- pivot 固定取第一个：已排序输入每轮只砍一个元素。

**追问。**
- 数据流里持续维护第 `k` 大？：大小为 `k` 的小根堆，堆顶即答案，每个新元素 `heappushpop`，`O(log k)`。
- 要第 `k` 大的不同元素？：先 `set(nums)` 去重再选。

**同模式。** LC 347 前 K 个高频元素、LC 973 最接近原点的 K 个点、LC 703 数据流中的第 K 大元素、LC 295 数据流的中位数
