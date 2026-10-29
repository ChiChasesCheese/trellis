---
id: tlc-successful-pairs-of-spells-and-potions-0-whole
node: a.successful-pairs-of-spells-and-potions
type: qa
---
## Q
**LC 2300 咒语和药水的成功对数**｜Medium · TikTok 高频

给两个正整数数组 `spells`（长度 `n`）和 `potions`（长度 `m`），`spells[i]` 是第 `i` 个咒语的能量，`potions[j]` 是第 `j` 瓶药水的能量，再给整数 `success`。咒语和药水的能量**相乘**大于等于 `success`，就是一对「成功」的组合。返回长度为 `n` 的数组 `pairs`，`pairs[i]` 是能与第 `i` 个咒语成功组合的药水数量。`1 <= n, m <= 10^5`，`1 <= spells[i], potions[j] <= 10^5`，`1 <= success <= 10^10`。例：`spells = [5,1,3]`，`potions = [1,2,3,4,5]`，`success = 7` → `[4,0,3]`；`spells = [3,1,2]`，`potions = [8,5,8]`，`success = 16` → `[2,0,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 药水排序一次；对每个咒语，二分找到药水里**第一个**满足 `药水 * 咒语 >= success` 的位置，它右边的药水全部成功，数量是 `m - 位置`。时间 `O((n + m) log m)`。

**识别。** 「对每个元素，统计另一个数组里满足阈值条件的个数」，且乘积对药水单调（药水越大乘积越大）：排序加二分的标准场景。`n = m = 10^5`，两两枚举 `10^10` 次，不可能；而「满足条件的药水构成排序后的一个后缀」这一事实让每个咒语只需一次二分。

**推导。** 暴力：双重循环，`O(n * m) = 10^10` → 药水排序后，对固定咒语 `s`，条件 `p * s >= success` 对 `p` 单调，满足条件的药水是一个后缀，二分找后缀起点 → 判定条件有两种写法：用整数向上取整求药水下限 `ceil(success / s)` 再 `bisect_left`；或者让 `bisect_left` 通过 `key` 参数直接比较乘积，避免手写取整。

```python
from bisect import bisect_left


def successful_pairs(spells: list[int], potions: list[int], success: int) -> list[int]:
    potions = sorted(potions)
    m = len(potions)
    # 对每个咒语 s：在有序药水里找第一个满足 p * s >= success 的位置，其右边全部成功
    return [m - bisect_left(potions, success, key=lambda p: p * s) for s in spells]
```

运行：`([5,1,3], [1,2,3,4,5], 7)` → `[4, 0, 3]`；`([3,1,2], [8,5,8], 16)` → `[2, 0, 2]`；`([1], [1], 1)` → `[1]`；`([1], [1], 2)` → `[0]`；`n = m = 10^5`、`success = 10^10` 约 `0.05` 秒。

**复杂度。** 时间 `O(m log m + n log m)`；空间 `O(m)`（排序后的药水）。

**易错点。**
- 用向下取整 `success // s` 当药水下限：`([2], [3, 4], 7)` 得到 `2`，正确是 `1`：`7 // 2 = 3`，但 `2 * 3 = 6 < 7`。需要向上取整 `-(-success // s)`。
- 用 `bisect_right` 代替 `bisect_left`：恰好等于 `success` 的组合被漏掉，`([2], [8, 8], 16)` 得到 `0`，正确是 `2`。
- 忘了给药水排序：二分对无序数组没有意义。
- 用浮点除法 `success / s` 当阈值：数值虽然在 `10^10` 以内可以精确表示，但比较时易因舍入出错，整数运算更稳妥。

**追问。**
- 咒语也排序，用双指针：咒语从小到大，成功药水从最大的一端数起，咒语变大时成功个数只增不减，指针只往一个方向走，总共 `O(n log n + m log m + n + m)`。
- 药水值域只有 `10^5`：做计数数组加后缀和，`suffix[v]` 是不小于 `v` 的药水个数，每个咒语 `O(1)` 查 `suffix[ceil(success / s)]`，总 `O(n + m + V)`。
- 药水动态增删：二分换成平衡树或树状数组，按值域计数。

**同模式。** LC 1498 满足条件的子序列数目、LC 475 供暖器、LC 744 寻找比目标字母大的最小字母、LC 2389 和有限的最长子序列、LC 1855 下标对中的最大距离。
