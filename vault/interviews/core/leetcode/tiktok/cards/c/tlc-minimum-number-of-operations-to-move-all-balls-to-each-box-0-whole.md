---
id: tlc-minimum-number-of-operations-to-move-all-balls-to-each-box-0-whole
node: c.minimum-number-of-operations-to-move-all-balls-to-each-box
type: qa
---
## Q
**LC 1769 移动所有球到每个盒子所需的最小操作数**｜Medium · LC TikTok 全时段热度 25/100

有 `n` 个盒子。给你一个长度为 `n` 的二进制字符串 `boxes`，`boxes[i]` 为 `'0'` 表示第 `i` 个盒子是空的，为 `'1'` 表示盒子里有一个小球。一步操作可以把一个小球移动到相邻的盒子（`abs(i - j) == 1`），移动后某些盒子可能有不止一个球。返回长度为 `n` 的数组 `answer`，`answer[i]` 是把所有小球移动到第 `i` 个盒子所需的最小操作数，每个 `answer[i]` 都根据盒子的**初始状态**计算。`n == boxes.length`，`1 <= n <= 2000`，`boxes[i]` 为 `'0'` 或 `'1'`。例：`boxes = "110"` → `[1,1,3]`；`boxes = "001011"` → `[11,8,5,4,3,4]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** `answer[i]` 就是所有小球到 `i` 的距离之和；从 `answer[i]` 推到 `answer[i + 1]` 时，`i` 左边（含 `i`）的球都远了 1，右边的球都近了 1，所以 `answer[i + 1] = answer[i] + 左边球数 - 右边球数`，`O(n)`。

**识别。** 「每个位置求一个到所有点的距离之和」：相邻位置之间的差只取决于左右两侧各有多少个点，可以由前一个答案 `O(1)` 推出（同类：LC 2602、LC 1685）。`n <= 2000` 允许 `O(n²)`，但递推更短也更快。

**推导。** 暴力：对每个 `i` 把所有球的距离加起来，`O(n²)`。第 0 个盒子的答案直接算出（球的下标之和）。从目标 `i` 移到 `i + 1`：下标 `<= i` 的球（`left` 个）距离各 `+1`；下标 `> i` 的球（`right` 个）距离各 `-1`；因此增量是 `left - right`。球数随扫描更新：经过 `i` 时若有球，它从右边转到左边。

**简单解法。** 不递推，对每个 `i` 直接把所有球的距离加起来。

```python
def min_operations_quadratic(boxes: str) -> list[int]:
    balls = [j for j, b in enumerate(boxes) if b == "1"]   # 所有球的位置
    return [sum(abs(i - j) for j in balls) for i in range(len(boxes))]
```

`O(n²)`，`n <= 2000` 约 400 万次运算，完全够用，可以直接当开场答案。

最优解：

```python
def min_operations(boxes: str) -> list[int]:
    right = boxes.count("1")                     # 目标 i 右边（下标 >= i+1 之后）的球数，初始为全部
    left = 0                                     # 目标 i 左边（下标 <= i）的球数
    cur = sum(j for j, b in enumerate(boxes) if b == "1")   # 目标是 0 时：每个球的距离就是它的下标
    ans: list[int] = []
    for i, b in enumerate(boxes):
        ans.append(cur)
        if b == "1":
            left += 1                            # 位置 i 的球，目标右移后属于「左边」
            right -= 1
        cur += left - right                      # 目标从 i 移到 i+1：左边的球远 1，右边的球近 1
    return ans
```

运行：`"110"` → `[1,1,3]`，`"001011"` → `[11,8,5,4,3,4]`；`"0"` → `[0]`，`"1"` → `[0]`，`"11111"` → `[10,7,6,7,10]`，`"0" * 2000` → 全 `0`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`（不计输出）。

**拓展优化。**
- 盒子里可以有多个球（输入变成整数列表 `counts`）：把 `b == "1"` 改成累加 `counts[i]`，其余完全不变。

**易错点。**
- `cur += left - right` 放在球数更新之前：`"110"` 得到 `[1,-1,-1]`，正确是 `[1,1,3]`；位置 `i` 的球要先算进 `left` 再递推。
- 先改 `cur` 再 `append`：答案整体错位，`"110"` 得到 `[1,3,5]`。

**追问。**
- 只要最小的那个答案：最优目标位置是球位置的中位数。
- 球有不同权重（每步代价不同）：左右的球数换成权重和，递推不变。

**同模式。** LC 2602 使数组元素全部相等的最少操作次数、LC 1685 有序数组中差绝对值之和、LC 296 最佳的碰头地点、LC 462 最小操作次数使数组元素相等 II、LC 834 树中距离之和。
