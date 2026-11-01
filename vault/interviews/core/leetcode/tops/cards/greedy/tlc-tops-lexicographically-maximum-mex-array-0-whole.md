---
id: tlc-tops-lexicographically-maximum-mex-array-0-whole
node: greedy.lexicographically-maximum-mex-array
type: qa
---
## Q
**LC 3948 字典序最大的 MEX 数组（Lexicographically Maximum MEX Array）**｜Hard · 全公司热度第 248 名

给你一个整数数组 `nums`。通过重复执行下面的操作构造数组 `result`，直到 `nums` 变为空：选择一个整数 `k`，满足 `1 <= k <= len(nums)`；计算 `nums` 的前 `k` 个元素的 MEX；把这个 MEX 附加到 `result`；从 `nums` 中移除前 `k` 个元素。返回执行这些操作后能得到的字典序最大的数组 `result`。数组的 MEX 是指数组中不包含的最小非负整数。如果两个数组在第一个不同的下标处，`a` 的元素大于 `b` 的对应元素，则 `a` 字典序更大；如果前 `min(a.length, b.length)` 个元素都相同，较长的数组字典序更大。`1 <= nums.length <= 10^5`，`0 <= nums[i] <= 10^5`。例：`nums = [0,1,0]` → `[2,1]`（先取 `[0,1]`，MEX 为 `2`，剩下 `[0]` 的 MEX 为 `1`）；`nums = [1,0,2]` → `[3]`；`nums = [3,1]` → `[0,0]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 贪心 + 后缀 MEX 预处理：每一步取「能拿到最大 MEX 的最短前缀」。

**一句话。** 当前剩余数组整体的 MEX 就是这一步能得到的最大值；取最短的、MEX 达到该值的前缀，其余留给后面的步骤。

**识别。** 「字典序最大」的构造题：从左往右每个位置都要尽量大，所以逐步贪心；MEX 随前缀变长只增不减，说明最大值出现在取完整个剩余数组时。`n = 10^5`，必须 `O(n)`。

**推导。** 枚举每一步的 `k` 再递归是指数级。观察两点：(1) 前缀越长 MEX 越大，所以这一步的最大值 = 剩余整个数组的 MEX，记为 `target`；(2) 达到 `target` 的前缀可能有很多个，取**最短**的：剩下的后缀是更长的数组，它能得到的结果不会更差（它能先吞下多出来的那几个元素，得到不小于原来的 MEX，再接上原来的步骤）。`target = 0` 时任何前缀的 MEX 都是 0，取 1 个元素，其余留给后面。后缀 MEX 用一个单调增的指针预处理，每段最短前缀只需顺序扫一遍。

```python
def max_mex_array(nums: list[int]) -> list[int]:
    n = len(nums)
    seen = [False] * (n + 2)
    suffix_mex = [0] * (n + 1)                    # suffix_mex[i] = nums[i:] 的 MEX
    mex = 0
    for i in range(n - 1, -1, -1):
        if nums[i] <= n:                          # MEX 不会超过 n，更大的数可以忽略
            seen[nums[i]] = True
        while seen[mex]:                          # 后缀往左扩，MEX 只增不减，指针单调
            mex += 1
        suffix_mex[i] = mex

    ans: list[int] = []
    i = 0
    while i < n:
        target = suffix_mex[i]                    # 前缀越长 MEX 越大：剩余整段的 MEX 就是这一步能得到的最大值
        got: set[int] = set()
        j = i
        while len(got) < target:                  # 取最短的前缀，凑齐 0..target-1
            if nums[j] < target:
                got.add(nums[j])
            j += 1
        ans.append(target)
        i = max(j, i + 1)                         # target = 0 时任何前缀 MEX 都是 0，只取 1 个元素，把其余留给后面
    return ans
```

运行：`[0,1,0]` → `[2, 1]`，`[1,0,2]` → `[3]`，`[3,1]` → `[0, 0]`，`[0]` → `[1]`，`[0,0,0]` → `[1, 1, 1]`，`[1,2,0,1,2,0]` → `[3, 3]`。

**复杂度。** 时间 `O(n)`：后缀 MEX 指针只前进，每个元素在构造阶段只被扫描一次；空间 `O(n)`。

**易错点。**
- 每一步都取整个剩余数组：`[0,1,0]` 得到 `[2]`，正确 `[2, 1]`；要取达到最大 MEX 的最短前缀，让后面还能再产出元素。
- `target = 0` 时也取一整段（比如取整个剩余数组）：`[3,1]` 得到 `[0]`，正确 `[0, 0]`；MEX 相同时拆得越多结果越长，字典序越大。
- 每一步都重新对剩余数组求 MEX：每次 `O(n)`，总共 `O(n²)`，`n = 10^5` 超时；用后缀 MEX 一次预处理。

**同模式。** LC 41 缺失的第一个正数、LC 55 跳跃游戏、LC 763 划分字母区间、LC 2598 执行操作后的最大 MEX。
