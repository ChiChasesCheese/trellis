---
slug: count-subarrays-with-majority-element-ii
---
## Q
**LC 3739 统计主要元素子数组数目 II**｜Hard

整数数组 `nums` 和整数 `target`。若一个子数组里 `target` 出现的次数严格大于子数组长度的一半，则 `target` 是它的主要元素。求主要元素为 `target` 的子数组个数。

## A
**一句话。** 把等于 `target` 的记 `+1`、其他记 `-1`，题目变成"和大于 `0` 的子数组个数"；前缀和每步只变 `±1`，所以"此前比当前小的前缀个数"可以 `O(1)` 递推。

```python
def count_majority_subarrays(nums, target):
    cnt = defaultdict(int)         # 前缀和 -> 出现次数
    cnt[0] = 1
    s = less = ans = 0             # less：此前前缀和 < s 的个数
    for x in nums:
        if x == target:
            less += cnt[s]         # 升到 s+1，原来等于 s 的现在更小
            s += 1
        else:
            s -= 1
            less -= cnt[s]         # 降到 s-1，等于新 s 的不再小于
        ans += less
        cnt[s] += 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先 `cnt[s] += 1` 再累加 `ans`：当前前缀不能算作"此前"的前缀。
- 降的时候先减 `less` 再改 `s`：顺序错了会减掉错误的计数。
- 要求"大于等于一半"：题目是严格大于，对应和 `> 0`。

**追问。**
- 比较的是哪两个前缀？：区间 `(i, j]` 的和 = `pre[j] - pre[i]`，大于 `0` 即 `pre[i] < pre[j]`。

**同模式。** LC 3737 统计主要元素子数组数目 I、LC 525 连续数组、LC 560 和为 K 的子数组、LC 974 和可被 K 整除的子数组
