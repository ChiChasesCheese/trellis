---
slug: split-array-into-consecutive-subsequences
---
## Q
**LC 659 分割数组为连续子序列**｜Medium

升序整数数组 `nums`。判断能否把它分成若干个子序列，每个子序列都是连续整数（相邻差 1）且长度至少为 3。

## A
**一句话。** 贪心：按顺序处理每个数，优先接到已有的以 `x - 1` 结尾的序列后面；接不上再尝试自己开一条 `x, x + 1, x + 2`；都不行就失败。

```python
def is_possible(nums):
    cnt = Counter(nums)          # 还没用的数
    tail = Counter()             # tail[x]：以 x 结尾的序列数
    for x in nums:
        if cnt[x] == 0:
            continue             # 已被前面的序列用掉
        cnt[x] -= 1
        if tail[x - 1] > 0:      # 优先续在已有序列后面
            tail[x - 1] -= 1
            tail[x] += 1
        elif cnt[x + 1] > 0 and cnt[x + 2] > 0:
            cnt[x + 1] -= 1      # 另起一条 x, x+1, x+2
            cnt[x + 2] -= 1
            tail[x + 2] += 1
        else:
            return False
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先尝试另起新序列：会把本可续写的数浪费，导致后面凑不够 3 个。
- 另起新序列时不检查 `x + 2`：长度必须至少 3。
- 忘了跳过已被用掉的数：`cnt[x] == 0` 时直接 `continue`。

**追问。**
- 为什么优先续写？：续写不增加序列数、不额外消耗后面的数，而且新开一条会占用 `x + 1`、`x + 2`，可能让其他数无处可去。
- 堆做法？：为每个结尾维护最小堆存序列长度，续写长度最短的，同样正确，`O(n log n)`。

**同模式。** LC 846 一手顺子、LC 1296 划分数组为连续数字的集合、LC 128 最长连续序列、LC 1743 从相邻元素对还原数组
