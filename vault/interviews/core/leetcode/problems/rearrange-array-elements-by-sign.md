---
slug: rearrange-array-elements-by-sign
---
## Q
**LC 2149 按符号重排数组**｜Medium

正负数各半，重排成正负交替、正数开头，且同号元素保持原顺序。

## A
**一句话。** 两个写指针：正数依次写到偶数下标，负数依次写到奇数下标。

```python
def rearrange_array(nums):
    ans = [0] * len(nums)
    pos, neg = 0, 1             # 下一个正数 / 负数的位置
    for x in nums:
        if x > 0:
            ans[pos] = x
            pos += 2
        else:
            ans[neg] = x
            neg += 2
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`（输出）。

**易错点。**
- 原地交换：会打乱同号元素的相对顺序。
- 负数从下标 `0` 开始写：要求正数开头。

**追问。**
- 正负数量不等（多的放末尾）？：交替写完少的一方，剩下的按序接在末尾。
- 必须原地、`O(1)` 空间？：保序原地重排要旋转子数组，`O(n^2)`。

**同模式。** LC 283 移动零、LC 905 按奇偶排序数组、LC 922 按奇偶排序数组 II
