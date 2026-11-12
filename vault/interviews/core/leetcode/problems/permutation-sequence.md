---
slug: permutation-sequence
---
## Q
**LC 60 排列序列**｜Hard

`[1..n]` 的全排列按字典序编号，给定 `n` 和 `k`，返回第 `k` 个排列。

## A
**一句话。** 阶乘进制逐位确定：固定首位后每块有 `(n-1)!` 个排列，`divmod(k, 块大小)` 得首位排名和块内名次。

```python
def get_permutation(n, k):
    digits = list(range(1, n + 1))    # 未用数字，升序
    k -= 1                            # 改成 0-based
    out = []
    for remaining in range(n, 0, -1):
        block = factorial(remaining - 1)
        q, k = divmod(k, block)       # q：首位排名，k：块内名次
        out.append(str(digits.pop(q)))
    return "".join(out)
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 忘了 `k -= 1`：`(3,3)` 得 `"231"`，应为 `"213"`；`(3,6)` 直接 `IndexError`。
- 块大小用 `factorial(remaining)`：`(3,3)` 得 `"132"`，应为 `"213"`。
- 取数字不删除（`digits[q]`）：数字重复，`(4,9)` 得 `"2211"`，应为 `"2314"`。

**追问。**
- 反问题（排列是第几个）？：逐位统计比当前位小且未用的数字个数乘对应阶乘，累加后加一。
- 有重复元素呢？：块大小改为多重集排列数 `n!/∏ 出现次数!`，每个候选首位的块大小不同。

**同模式。** LC 46 全排列、LC 47 全排列 II、LC 31 下一个排列、LC 440 字典序的第K小数字
