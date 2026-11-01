---
id: tlc-tops-concatenation-of-array-0-whole
node: arrays-hashing.concatenation-of-array
type: qa
---
## Q
**LC 1929 数组串联**｜Easy · 全公司热度第 185 名

给你一个长度为 `n` 的整数数组 `nums`，构造长度为 `2n` 的数组 `ans`，对所有 `0 <= i < n` 满足 `ans[i] == nums[i]` 且 `ans[i + n] == nums[i]`，即 `ans` 由两个 `nums` 串联而成，返回 `ans`。`n == nums.length`，`1 <= n <= 1000`，`1 <= nums[i] <= 1000`。例：`nums = [1,2,1]` → `[1,2,1,1,2,1]`；`nums = [1,3,2,1]` → `[1,3,2,1,1,3,2,1]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 数组拼接与下标映射；列表是引用类型，别改到输入。

**一句话。** 两个 `nums` 首尾相接，即 `nums + nums`，生成新列表。

**识别。** 「`ans[i]` 与 `ans[i + n]` 都等于 `nums[i]`」就是把数组重复两遍；`n <= 1000`，无复杂度压力，考点是语言基础和不要破坏输入。

**推导。** 一次遍历把 `nums[i]` 同时写进 `ans[i]` 和 `ans[i + n]` 是 `O(n)`；`+` 在 C 层做同样的事，更短，复杂度一样。

```python
def get_concatenation(nums: list[int]) -> list[int]:
    return nums + nums  # 新列表：前 n 个是 nums[i]，后 n 个 ans[i + n] 也是 nums[i]
```

运行：`[1,2,1]` → `[1,2,1,1,2,1]`；`[1,3,2,1]` → `[1,3,2,1,1,3,2,1]`；`[5]` → `[5,5]`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（输出）。

**拓展优化。**
- 面试官要求手写、不用 `+`（对应 C++ / Java 的写法）：先开 `2n` 的数组，再一趟把每个值写到两个位置：

```python
def get_concatenation_loop(nums: list[int]) -> list[int]:
    n = len(nums)
    ans = [0] * (2 * n)
    for i, x in enumerate(nums):
        ans[i] = ans[i + n] = x  # 直接对应题目里的两条下标关系
    return ans
```

**易错点。**
- `ans = nums` 后 `ans += nums` 或 `nums.extend(nums)`：`+=` 就地修改，调用方的 `nums = [1,2,1]` 变成 `[1,2,1,1,2,1]`，返回值虽对，输入被破坏。
- `[nums] * 2` 得到 `[[1,2,1],[1,2,1]]`，是嵌套列表，不是长度 `2n` 的一维数组；`nums * 2` 才是 `[1,2,1,1,2,1]`。
- 边写边遍历：`for x in nums: nums.append(x)` 永远不会结束，因为遍历的列表在变长。

**同模式。** LC 1920 基于排列构建数组、LC 1470 重新排列数组、LC 1480 一维数组的动态和、LC 189 轮转数组。
