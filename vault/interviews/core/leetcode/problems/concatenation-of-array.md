---
slug: concatenation-of-array
---
## Q
**LC 1929 数组串联**｜Easy

返回由两个 `nums` 首尾串联成的长度 `2n` 的数组。

## A
**一句话。** 直接 `nums + nums`，生成新列表。

```python
def get_concatenation(nums):
    return nums + nums
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- `nums += nums` 或 `nums.extend(nums)`：就地修改，调用方的输入被破坏。
- `[nums] * 2`：得到嵌套列表 `[[1,2,1],[1,2,1]]`，要用 `nums * 2`。
- `for x in nums: nums.append(x)`：边遍历边变长，永不结束。

**追问。**
- 重复 `k` 次怎么写？：`nums * k`。

**同模式。** LC 1920 基于排列构建数组、LC 1470 重新排列数组、LC 1480 一维数组的动态和、LC 189 轮转数组
