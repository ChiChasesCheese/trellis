---
slug: make-lexicographically-smallest-array-by-swapping-elements
---
## Q
**LC 2948 交换得到字典序最小的数组**｜Medium

可交换任意两个下标，当且仅当二者的值之差不超过 `limit`。求任意次交换后字典序最小的数组。

## A
**一句话。** 按值排序，相邻差不超过 `limit` 的连成一组，组内可任意换位，小值放到靠前的位置。

```python
def lexicographically_smallest_array(nums, limit):
    n = len(nums)
    order = sorted(range(n), key=nums.__getitem__)  # 按值排下标
    ans = nums[:]
    i = 0
    while i < n:
        j = i + 1                  # 相邻值差 <= limit 连成一组
        while (j < n and
               nums[order[j]] - nums[order[j-1]] <= limit):
            j += 1
        group = order[i:j]         # 这组的下标，按值升序
        for pos, idx in zip(sorted(group), group):
            ans[pos] = nums[idx]   # 靠前的位置拿最小值
        i = j
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 整个数组直接排序：`[1,7,6,18,2,1]`、`limit=3` 得 `[1,1,2,6,7,18]`，`18` 不能动。
- 与组内第一个值比较而不是相邻值：`[5,3,1]`、`limit=2` 会把 `5` 分出去。
- 组内位置不排序就写回：`[1,5,3,9,8]` 会原样返回。

**追问。**
- 为什么相邻差够用？：连通性可传递，`a~b`、`b~c` 就能通过一串交换让 `a`、`c` 换位。
- 用并查集怎么做？：排序后相邻差 `<= limit` 就合并，再按根分组，效果相同。

**同模式。** LC 1202 交换字符串中的元素、LC 721 账户合并、LC 947 移除最多的同行或同列石头
