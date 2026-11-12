---
slug: missing-ranges
---
## Q
**LC 163 缺失的区间**｜Easy

升序数组 `nums`（元素互异，都在 `[lower, upper]` 内），返回恰好覆盖区间内所有缺失数的最小有序区间列表。

## A
**一句话。** 首尾补哨兵 `lower-1`、`upper+1`，相邻已知数差 `>= 2` 时中间就是一段缺失区间。

```python
def find_missing_ranges(nums, lower, upper):
    ans = []
    prev = lower - 1             # 哨兵
    for x in chain(nums, (upper + 1,)):
        if x - prev >= 2:
            ans.append([prev + 1, x - 1])
        prev = x
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉尾哨兵：`[0,1,3,50,75]`, `0`, `99` 少了 `[76,99]`。
- 判断写成 `x - prev > 2`：只缺一个数的 `[2,2]` 被漏掉。

**追问。**
- 输出成 `"2"`、`"4->49"` 的字符串？：`a == b` 写 `str(a)`，否则 `f"{a}->{b}"`。
- `nums` 有重复怎么办？：差为 `0` 不产生区间，代码不用改。

**同模式。** LC 228 汇总区间、LC 56 合并区间、LC 57 插入区间、LC 352 将数据流变为不相交区间
